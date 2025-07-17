from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_transcribe_view, name='live_transcribe'),
    path('transcribe-chunk/', views.transcribe_chunk, name='transcribe_chunk'),
]
