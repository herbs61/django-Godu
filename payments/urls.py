from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.payment, name='payment'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('edit/<int:payment_id>/', views.edit, name='edit'),
    path('delete/<int:payment_id>/', views.delete, name='delete'),
    path('callback/', views.payment_callback, name='payment_callback'),  # Redirect to payment view
]