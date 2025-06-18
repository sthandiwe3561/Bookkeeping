from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from decimal import Decimal
from django.conf import settings
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer

from .models import Customer,User,ServiceRecord,Invoice,Expense


# Create your views here.
#login
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "bookkeeping/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bookkeeping/login.html")
    
 #logout   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


#register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bookkeeping/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "bookkeeping/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "bookkeeping/register.html")
    
#INDEX FUNCTION
def index(request):
    return render(request, "bookkeeping/index.html")

#dashboard
def dashboard(request):
    return render(request, "bookkeeping/dashboard.html")

#customers management function
def customers(request,post_id=None):

      #fetch all the list of the customers
    customers_lists = Customer.objects.filter(user=request.user)
    first_customer = customers_lists.first()


    if post_id:
        customer = get_object_or_404(Customer, id=post_id,user=request.user)
    else:
        customer = None

    if request.method == "POST":

        #fetching the data from the input
       name = request.POST.get("name")
       email = request.POST.get("email")
       phone_number = request.POST.get("phoneNo")
       estate_name = request.POST.get("estate")
       plot_number = request.POST.get("plot")
       
           # Check if any of the fields are empty
       if not all([name, email, phone_number, estate_name, plot_number]):
            error = "All fields are required. Please fill in everything."
            return render(request, "bookkeeping/customers.html", {'error': error, 'customers':customers_lists, 'post':customer})
       
       if customer:
            # Update existing customer
            customer.name = name
            customer.email = email
            customer.phone_no = phone_number
            customer.estate = estate_name
            customer.plot_no = plot_number
            customer.save()
            messages.success(request, "Customer updated successfully!")
            return redirect(reverse('customer_form') + f'?highlight=customer-{customer.id}') #type: ignore
          
       else:
            # Create new customer
           new_customer: Customer = Customer.objects.create(
                name=name,
                email=email,
                phone_no=phone_number,
                estate=estate_name,
                plot_no=plot_number,
                user=request.user  # Make sure to assign the current user

            )
       messages.success(request, "Customer added successfully!")
       return redirect(reverse('customer_form') + f'?highlight=customer-{new_customer.id}') #type: ignore
    

    return render(request, "bookkeeping/customers.html", {
        'customers': customers_lists,
        'post': customer,
        'default_customer': first_customer
    })
    

def customers_view(request):
    #fetch all the list of the customers
    customers_lists = Customer.objects.filter(user=request.user)
    first_customer = customers_lists.first()
    print("First customer:", first_customer)


    return render(request,"bookkeeping/customers.html",{'customers':customers_lists,        
                                                        'default_customer': first_customer})

@api_view(['GET'])
def customer_api(request, id):
    customer = Customer.objects.get(id=id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

def customer_delete(request, post_id):
    # Get the customer to delete (make sure it's the current user's)
    customer_to_delete = get_object_or_404(Customer, id=post_id, user=request.user)

    # Try to get the next customer (by ID)
    next_customer = Customer.objects.filter(user=request.user, id__gt=post_id).order_by('id').first()

    # If there’s no next one, try the previous one
    if not next_customer:
        next_customer = Customer.objects.filter(user=request.user, id__lt=post_id).order_by('-id').first()

    # Store ID for redirect highlight
    highlight_id = next_customer.id if next_customer else "" #type: ignore

    # Delete the customer
    customer_to_delete.delete()

    # Redirect with highlight_id (if any)
    if highlight_id:
        return redirect(reverse('customer_form') + f'?highlight=customer-{highlight_id}')
    else:
        return redirect('customer_form')

#services history
def add_service(request):
    customers = Customer.objects.filter(user=request.user)
    services = ServiceRecord.objects.all()


    if request.method == "POST":
        #fetching the data from the input
        service_type = request.POST.get("service_type", "normal")  # Default to normal if not specified
        # Common fields
        description = request.POST.get("description")
        price = request.POST.get("price")
        service_date = request.POST.get("service_date")
        #normals service
        customer_id = request.POST.get("customer")
        special_load = request.POST.get("special_load")
        #specail service
        client_name = request.POST.get("client_name")
        client_phone = request.POST.get("client_phone")

        service = ServiceRecord(
            service_type=service_type,
            service_description=description,
            price=price,
            service_date=service_date,
        )

        if service_type == "normal":
            customer = Customer.objects.filter(id=customer_id, user=request.user).first()
            service.customer = customer
            service.customer_name_backup = customer.name if customer else "" #type: ignore
            service.special_load = special_load or ""
        else:
            service.client_name = client_name
            service.client_phone = client_phone

        service.save()

        action = request.POST.get("action")
        if action == "save_continue":
            return redirect("add_service")  # same page to add more
        else:
            return redirect(reverse('add_service') + f'?highlight=service-{service.id}') #type: ignore

    return render(request, "bookkeeping/service_history.html", {
        "customers": customers,
        "post": None,
        "services":services,
    })


def service_delete(request, post_id):
    # Get the customer to delete (make sure it's the current user's)
    service_to_delete = get_object_or_404(ServiceRecord, id=post_id)

    # Try to get the next customer (by ID)
    next_service = ServiceRecord.objects.filter(id__gt=post_id).order_by('id').first()

    # If there’s no next one, try the previous one
    if not next_service:
        next_service = ServiceRecord.objects.filter(id__lt=post_id).order_by('-id').first()

    # Store ID for redirect highlight
    highlight_id = next_service.id if next_service else "" #type: ignore

    # Delete the customer
    service_to_delete.delete()

    # Redirect with highlight_id (if any)
    if highlight_id:
        return redirect(reverse('add_service') + f'?highlight=service-{highlight_id}')
    else:
        return redirect('add_service')


def edit_service(request, record_id):
    service = get_object_or_404(ServiceRecord, id=record_id)
    customers = Customer.objects.filter(user=request.user)

    if request.method == "POST":
        service.service_type = request.POST.get("service_type", "normal")
        service.service_description = request.POST.get("description")
        service.price = request.POST.get("price")
        service.service_date = request.POST.get("service_date")

        if service.service_type == "normal":
            customer_id = request.POST.get("customer")
            special_load = request.POST.get("special_load")
            customer = Customer.objects.filter(id=customer_id, user=request.user).first()
            service.customer = customer
            service.customer_name_backup = customer.name if customer else ""
            service.special_load = special_load or ""
            service.client_name = ""
            service.client_phone = ""
        else:
            service.client_name = request.POST.get("client_name")
            service.client_phone = request.POST.get("client_phone")
            service.customer = None
            service.customer_name_backup = ""
            service.special_load = ""

        service.save()
        return redirect(reverse('add_service') + f'?highlight=service-{service.id}') #type: ignore

    return render(request, "bookkeeping/service_history.html", {
        "post": service,
        "customers": customers
    })


def service_list_filter(request):
    services = ServiceRecord.objects.all()

    name_query = request.GET.get("name", "").strip()
    month_query = request.GET.get("month", "").strip()

    if name_query:
        services = services.filter(
            Q(customer_name_backup__icontains=name_query) |
            Q(client_name__icontains=name_query)
        )

    if month_query:
        try:
            year, month = map(int, month_query.split("-"))
            services = services.filter(
                service_date__year=year,
                service_date__month=month
            )
        except ValueError:
            pass  # Invalid input — skip filter

    return render(request, "bookkeeping/service_history.html", {
        "services": services,
    })

@api_view(['GET'])
def service_by_name_api(request):
    name = request.GET.get("name")
    services = ServiceRecord.objects.filter(
        Q(customer_name_backup__iexact=name) | Q(client_name__iexact=name),
        invoice__isnull=True  # only unbilled
    )
    data = [
        {
            "id": s.id,#type: ignore
            "service_description": s.service_description,
            "price": float(s.price),
            "date": s.service_date
        } for s in services
    ]
    return Response(data)

def invoice_page(request):
    services = ServiceRecord.objects.filter(invoice__isnull=True)
    invoices = Invoice.objects.all()
    return render(request,"bookkeeping/invoice_gen.html",{"services":services,
                                                          "invoices":invoices
                                                          })

def create_invoice(request):
        if request.method == "POST":
            service_ids = request.POST.getlist("selected_services")
            services = ServiceRecord.objects.filter(id__in=service_ids)

            # Determine client name or customer (assuming all services are for one client/customer)
            first_service = services.first()
            customer = None
            client_name = ""

            if first_service:
                 if first_service.service_type == "special":
                     client_name = first_service.client_name
                 else:
                     customer = first_service.customer

                     # Optional fallback
                     if not customer and first_service.customer_name_backup:
                          client_name = first_service.customer_name_backup

            # Calculate total amount
            total_amount = sum(service.price for service in services)

            # Create the invoice
            invoice = Invoice.objects.create(
                      customer=customer,
                      client_name=client_name,
                      total_amount=Decimal(total_amount),
                      created_by=request.user,
                    )
            
            # Link services to invoice
            services.update(invoice=invoice)  # Optional, since M2M is already set

            return redirect('invoice_page')


def invoice_display(request,invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    show_download_button = request.GET.get("download") == "true"



    context = {
    'invoice': invoice,
    'company_name': "The Horses Garden Services",
    'company_address': "3561 Mpophomeni, Merrival, 3291",
    'company_phone': "072 123 4567",
    'show_download_button': show_download_button,  # 🆕
   }
    return render(request,"bookkeeping/generated_invoice.html",context)


            

#download invoice function
def download_invoice_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    context = {
        "invoice": invoice,
        "company_name": "The Horses Garden Services",
        "company_address": "3561 Mpophomeni, Merrival, 3291",
        "company_phone": "072 123 4567",
        "show_download_button": False,  # optional: don't show button in PDF
        "pdf_export": True  # Tell the template to hide nav

    }

    template = get_template("bookkeeping/generated_invoice.html")
    html = template.render(context)

    css_path = finders.find("bookkeeping/invoice.css")
    if isinstance(css_path, list):
        css_path = css_path[0]

    if css_path:
        with open(css_path) as css_file:
            css = css_file.read()
        html = html.replace("</head>", f"<style>{css}</style></head>")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=invoice_{invoice_id}.pdf"
    pisa.CreatePDF(html, dest=response)

    return response

# invoice api to delete
@api_view(["DELETE"])
def delete_invoice(request, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.delete()
        return Response({"message": "Invoice deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    except Invoice.DoesNotExist:
        return Response({"error": "Invoice not found."}, status=status.HTTP_404_NOT_FOUND)
    

#expenses
#create and save expenses function
def create_expense(request):
    expenses = Expense.objects.all()
    if request.method == "POST":
        selected_category = request.POST.get("expense_category")
        price = request.POST.get("price")
        date = request.POST.get("date")

        expense = Expense(
            user = request.user,
            price = price,
            expense = selected_category,
            expense_date = date
        )
        expense.save()  # ✅ Save the expense to the database

        return redirect('add_expense')

    return render(request,"bookkeeping/expense.html",{'expenses':expenses})
    

  


