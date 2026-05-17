from django.contrib import admin
from django.urls import path

from dizimus.config.api import api




urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]