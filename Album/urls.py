from django.urls import path
from Album import views

app_name = 'Album'

urlpatterns = [
    path('', views.img_list, name='img_list'),
    path('<str:requested_run>', views.img_list, name='img_list'),
]