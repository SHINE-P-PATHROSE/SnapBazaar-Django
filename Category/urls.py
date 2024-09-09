from django.urls import path
from . import views
from .views import CategoryDetailView

urlpatterns = [
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),  # Detail view for a specific category
]