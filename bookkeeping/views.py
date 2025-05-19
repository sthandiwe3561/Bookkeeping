from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomerSerializer

from .models import Customer


# Create your views here.
#INDEX FUNCTION
def dashboard(request):
    return render(request, "bookkeeping/dashboard.html")

#customers management function
def customers(request,post_id=None):

      #fetch all the list of the customers
    customers_lists = Customer.objects.all()
    first_customer = customers_lists.first()


    if post_id:
        customer = get_object_or_404(Customer, id=post_id)

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
       else:
            # Create new customer
            Customer.objects.create(
                name=name,
                email=email,
                phone_no=phone_number,
                estate=estate_name,
                plot_no=plot_number
            )
       messages.success(request, "Customer added successfully!")
       return redirect('customer_form')


    return render(request, "bookkeeping/customers.html", {
        'customers': customers_lists,
        'post': customer,
        'default_customer': first_customer
    })
    

def customers_view(request):
    #fetch all the list of the customers
    customers_lists = Customer.objects.all()
    first_customer = customers_lists.first()
    print("First customer:", first_customer)


    return render(request,"bookkeeping/customers.html",{'customers':customers_lists,        
                                                        'default_customer': first_customer})

@api_view(['GET'])
def customer_api(request, id):
    customer = Customer.objects.get(id=id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)

def customer_delete(request,post_id):
     #fecthing the users id     
    customers_lists = get_object_or_404(Customer, id=post_id)

    customers_lists.delete()

       #fetch all the list of the customers
    customers_lists = Customer.objects.all()
    return redirect('customer_form')



