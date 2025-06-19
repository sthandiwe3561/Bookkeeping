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
    path("invoice_page",views.invoice_page,name="invoice_page"),
    path("create_invoice",views.create_invoice,name="create_invoice"), #type: ignore
    path('invoice_display/<int:invoice_id>/', views.invoice_display, name='invoice_display'),
    path("invoice/<int:invoice_id>/download/", views.download_invoice_pdf, name="download_invoice_pdf"),
    path('api/invoices/<int:invoice_id>/delete/', views.delete_invoice, name='delete_invoice_api'),
    path("add_expense", views.create_expense, name="add_expense"),
    path('expense_delete/<int:post_id>/', views.expense_delete, name='expense_delete'),
    path("add_loan", views.create_loan, name="add_loan"),
    path('loan_delete/<int:post_id>/', views.loan_delete, name='loan_delete'),

]
