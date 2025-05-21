from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer

from .models import Customer,User


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
            return redirect(reverse('customer_form') + f'?highlight_id={customer.id}') #type: ignore
          
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
       return redirect(reverse('customer_form') + f'?highlight_id={new_customer.id}') #type: ignore
    

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
        return redirect(reverse('customer_form') + f'?highlight_id={highlight_id}')
    else:
        return redirect('customer_form')






