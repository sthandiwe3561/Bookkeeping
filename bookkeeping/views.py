from django.shortcuts import render,redirect

from .models import Customer


# Create your views here.
#INDEX FUNCTION
def dashboard(request):
    return render(request, "bookkeeping/dashboard.html")

#customers management function
def customers(request):

    if request.method == "POST":

        #fetching the data from the input
       name = request.POST.get("name")
       email = request.POST.get("email")
       phone_number = request.POST.get("phoneNo")
       estate_name = request.POST.get("estate")
       plot_number = request.POST.get("plot")

       #create
       Customer.objects.create(
                name = name,  
                email = email,
                phone_no = phone_number,
                estate = estate_name,
                plot_no = plot_number)
       return redirect(customers)
    else:
        return render(request, "bookkeeping/customers.html")
    