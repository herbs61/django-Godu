from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/', views.index, name='driver'),
    path('create/', views.create, name='create_driver'),
    # path('edit/<int:driver_id>/', views.edit, name='edit_driver'),
    # path('delete/<int:driver_id>/', views.delete, name='delete_driver'),
   



]