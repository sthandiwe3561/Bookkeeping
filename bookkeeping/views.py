from django.shortcuts import render

# Create your views here.
#INDEX FUNCTION
def dashboard(request):
    return render(request, "bookkeeping/dashboard.html")