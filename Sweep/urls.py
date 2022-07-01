from django.urls import path
from Sweep import views

app_name = 'Sweep'

urlpatterns = [
    path('', views.get_run_keys, name='get_run_keys'),
]