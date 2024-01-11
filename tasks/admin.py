import pickle

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin[Task]):
    list_display = ("id", "func", "created_at")
    list_filter = ("func",)
    readonly_fields = (
        "func_args",
        "func_kargs",
        "queued",
    )

    def func_args(self, obj: Task):
        return pickle.loads(obj.args)

    def func_kargs(self, obj: Task):
        return pickle.loads(obj.kargs)
