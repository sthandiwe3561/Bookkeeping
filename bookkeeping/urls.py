from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("customer_form", views.customers, name="customer_form"),
    path("customer_form_edit/<int:post_id>/", views.customers, name="customer_form_edit"),

    path('customer_delete/<int:post_id>/', views.customer_delete, name='customer_delete'),

    
]
