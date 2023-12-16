

# downloader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.download_playlist, name='download_playlist'),
]
