from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("login", views.login_view, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("customer_form", views.customers, name="customer_form"),
    path("add_service", views.add_service, name="add_service"),
    path('customers/', views.customers_view, name='customers'),
    path("customers/edit/<int:post_id>/", views.customers, name="customer_form_edit"),
    path('api/customers/<int:id>/', views.customer_api, name='customer_api'),
    path('customers/delete/<int:post_id>/', views.customer_delete, name='customer_delete'),
    path('services_delete/<int:post_id>/', views.service_delete, name='service_delete'),
    path("services_edit/<int:record_id>/", views.edit_service, name="service_edit"),
    path("service_list_fiilter",views.service_list_filter, name="service_list_filter"),
    path('api/service-by-name/', views.service_by_name_api, name='service_api'),
    path("invoice_page",views.invoice_page,name="invoice_page")

    
]
