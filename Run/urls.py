from django.urls import path
from Run import views
from Sweep import views as Sweepviews
app_name = 'Run'

urlpatterns = [
    path('', Sweepviews.get_run_keys, name='Sweep_get_run_keys'),
    path('listed', views.get_run_keys, name='get_run_keys'),
    path('<str:requested_run_key>', views.get_meta_data, name='get_meta_data'),
]