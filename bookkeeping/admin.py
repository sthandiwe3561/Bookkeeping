from django.contrib import admin
from .models import Customer, User,ServiceRecord

# Register your models here.
admin.site.register(Customer)
admin.site.register(User)
admin.site.register(ServiceRecord)


