from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),  # Handles order placement
    path('payments/', views.payments, name='payments'),            # Handles payment processing
    path('order_complete/', views.order_complete, name='order_complete'),  # Displays order completion page
]
