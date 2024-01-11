import multiprocessing
from typing import Any

from django.core.management import BaseCommand
from django.core.management.base import CommandParser

from ...listeners import listen_for_queued, listen_for_scheduled


class Command(BaseCommand):
    help = "Listen for tasks."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "--processes",
            type=int,
            dest="processes",
            default=1,
        )

    def handle(self, *args: Any, **options: Any):
        processes: int = options["processes"]
        multiprocessing.set_start_method("fork", force=True)

        for i in range(processes):
            process = multiprocessing.Process(
                name=f"listen_for_queued_{i}",
                target=listen_for_queued,
            )
            process.start()

        listen_for_scheduled()
