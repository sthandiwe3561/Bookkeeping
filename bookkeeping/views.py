from django.shortcuts import render,redirect

from .models import Customer


# Create your views here.
#INDEX FUNCTION
def dashboard(request):
    return render(request, "bookkeeping/dashboard.html")

#customers management function
def customers(request):

      #fetch all the list of the customers
    customers_lists = Customer.objects.all()

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
            return render(request, "bookkeeping/customers.html", {'error': error, 'customers':customers_lists})

       #create
       Customer.objects.create(
                name = name,  
                email = email,
                phone_no = phone_number,
                estate = estate_name,
                plot_no = plot_number)
       success = "Customer added successfully!"
       return render(request, "bookkeeping/customers.html",{'customers':customers_lists, 'success':success})

    else:
        return render(request, "bookkeeping/customers.html",{'customers':customers_lists})

def customers_list(request):
    #fetch all the list of the customers
    customers_lists = Customer.objects.all()
    return render(request,"bookkeeping/customers.html",{'customers':customers_lists})