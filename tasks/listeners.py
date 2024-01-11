import multiprocessing
import select
from typing import TYPE_CHECKING

from django.db import connection
from django.utils import timezone

from . import CHANNEL_QUEUED, CHANNEL_SCHEDULED, POLL_TIMEOUT
from .models import Task
from .tasks import execute_task

if TYPE_CHECKING:
    from psycopg2._psycopg import connection as Connection


def listen_for_scheduled():
    multiprocessing.set_start_method("fork", force=True)
    cursor = connection.cursor()
    pg_connection: Connection = connection.connection

    cursor.execute(f'LISTEN "{CHANNEL_SCHEDULED}";')

    Task.objects.filter(queued=True).update(queued=False)

    while True:
        next_timestamp = float("inf")

        for task in Task.objects.filter(queued=False).order_by("queue_at").iterator():
            if task.queue_at and task.queue_at > timezone.now():
                next_timestamp = task.queue_at.timestamp()
                break

            Task.objects.filter(id=task.id).update(queued=True)
            cursor.execute(f"SELECT pg_notify('{CHANNEL_QUEUED}', '{task.id}');")

        while (remaining := next_timestamp - timezone.now().timestamp()) > 0:
            timeout = min(remaining, POLL_TIMEOUT)
            if select.select([pg_connection], [], [], timeout) != ([], [], []):
                pg_connection.poll()
                while pg_connection.notifies:
                    notification = pg_connection.notifies.pop(0)
                    timestamp = float(notification.payload)
                    if next_timestamp > timestamp:
                        next_timestamp = timestamp


def listen_for_queued():
    multiprocessing.set_start_method("fork", force=True)
    cursor = connection.cursor()
    pg_connection: Connection = connection.connection

    cursor.execute(f'LISTEN "{CHANNEL_QUEUED}";')

    while True:
        if select.select([pg_connection], [], [], POLL_TIMEOUT) != ([], [], []):
            try:
                pg_connection.poll()
                while pg_connection.notifies:
                    notification = pg_connection.notifies.pop(0)
                    execute_task(int(notification.payload))
            except Exception as e:
                connection.close()
                process = multiprocessing.Process(target=listen_for_queued)
                process.start()
                raise e
