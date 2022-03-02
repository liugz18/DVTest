from django.urls import path
from Run import views

app_name = 'Run'

urlpatterns = [
    path('', views.get_run_keys, name='get_run_keys'),
    path('<str:requested_run_key>', views.get_meta_data, name='get_meta_data'),
]