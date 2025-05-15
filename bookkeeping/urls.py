from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("customer_form", views.customers, name="customer_form")
    
]
