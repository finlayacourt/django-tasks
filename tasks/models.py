from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    queue_at = models.DateTimeField(null=True)
    queued = models.BooleanField()

    func = models.CharField(max_length=255)
    args = models.BinaryField()
    kargs = models.BinaryField()

    def __str__(self):
        return f"{self.id} - {self.func}"
