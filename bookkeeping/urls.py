from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("customer_form", views.customers, name="customer_form"),
    path('customers/', views.customers_view, name='customers'),
    path("customers/edit/<int:post_id>/", views.customers, name="customer_form_edit"),
    path('api/customers/<int:id>/', views.customer_api, name='customer_api'),
    path('customers/delete/<int:post_id>/', views.customer_delete, name='customer_delete'),


    
]
