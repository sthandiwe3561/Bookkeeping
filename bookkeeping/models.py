from django.contrib.auth.models import AbstractUser
from datetime import date
from django.db import models

# Create your models here.
class User(AbstractUser):
      groups = models.ManyToManyField(
        'auth.Group',
        related_name='+',
        related_query_name='+',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
      user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='+',
        related_query_name='+',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
  

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    estate = models.CharField(max_length=100)
    plot_no = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, editable=False, blank=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    client_name = models.CharField(max_length=255, blank=True)
    date_issued = models.DateField(default=date.today)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

#FUNCTON THAT GENERATE THE UNIQUE CODE FOR EACH INVOICE CREATED
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by('-id').first()
            if last_invoice and last_invoice.invoice_number:
                try:
                    last_number = int(last_invoice.invoice_number.split('-')[1])
                except (IndexError, ValueError):
                    last_number = 0
            else:
                last_number = 0

            new_number = last_number + 1
            self.invoice_number = f"INV-{new_number:03}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number

class ServiceRecord(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('normal', 'Normal Service'),
        ('special', 'Special Once-Off Service'),
    ]

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE_CHOICES, default='normal')

    # For 'normal' services
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name_backup = models.CharField(max_length=255, blank=True)  # 🆕 This stores the name
    special_load = models.CharField(max_length=255, blank=True)  # Optional

    # For 'special' once-off services
    client_name = models.CharField(max_length=255, blank=True)
    client_phone = models.CharField(max_length=20, blank=True)

    service_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    service_date = models.DateField(default=date.today)
    invoice = models.ForeignKey(Invoice, null=True, blank=True, on_delete=models.SET_NULL, related_name="services")


    def __str__(self):
        if self.service_type == 'normal':
            return f"{self.customer.name if self.customer else self.customer_name_backup} on {self.service_date}"
        return f"Special - {self.client_name} on {self.service_date}"

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expense")
    expense = models.CharField(max_length=20, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField(default=date.today)

    def __str__(self):
        return self.expense

class Loans(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan")
    name = models.CharField(max_length=20, blank=True)
    loan_reason = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    loan_date = models.DateField(default=date.today)
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    ]
    loan_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return self.name


