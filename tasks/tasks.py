import datetime
import pickle
from importlib import import_module
from typing import Any

from django.db import connection, transaction

from . import CHANNEL_QUEUED, CHANNEL_SCHEDULED
from .models import Task


def defer(func: str, *args: Any, **kwargs: Any):
    task = Task.objects.create(
        queue_at=None,
        queued=True,
        func=func,
        args=pickle.dumps(args),
        kargs=pickle.dumps(kwargs),
    )

    with connection.cursor() as cursor:
        cursor.execute(f"select pg_notify('{CHANNEL_QUEUED}', '{task.id}');")


def schedule(at: datetime.datetime, func: str, *args: Any, **kwargs: Any):
    Task.objects.create(
        queue_at=at,
        queued=False,
        func=func,
        args=pickle.dumps(args),
        kargs=pickle.dumps(kwargs),
    )

    with connection.cursor() as cursor:
        cursor.execute(f"select pg_notify('{CHANNEL_SCHEDULED}', '{at.timestamp()}');")


@transaction.atomic
def execute_task(id: int):
    task = Task.objects.select_for_update(skip_locked=True).filter(id=id).first()
    if task:
        module, name = task.func.rsplit(".", 1)
        func = getattr(import_module(module), name)
        args = pickle.loads(task.args)
        kargs = pickle.loads(task.kargs)
        func(*args, **kargs)
        task.delete()
