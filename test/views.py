import datetime

from django import forms
from django.http import HttpRequest
from django.shortcuts import render
from django.utils import timezone

from tasks.tasks import defer, schedule


class MessageForm(forms.Form):
    message = forms.CharField(label="Message", max_length=100)
    delay = forms.IntegerField(label="Seconds", required=False)


def index(request: HttpRequest):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            delay = form.cleaned_data["delay"]
            if delay:
                schedule(
                    timezone.now() + datetime.timedelta(seconds=delay),
                    "test.views.print_message",
                    message,
                )
            else:
                defer("test.views.print_message", message)
    else:
        form = MessageForm()

    return render(request, "index.html", {"form": form})


def print_message(message: str):
    print(f'received "{message}"')
