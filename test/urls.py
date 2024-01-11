"""Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.
"""

from test.views import index

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
]
