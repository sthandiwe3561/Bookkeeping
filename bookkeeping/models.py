from django.contrib.auth.models import AbstractUser
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
    plot_no = models.IntegerField()

    def __str__(self):
        return self.name

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
    service_date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.service_type == 'normal':
            return f"{self.customer.name if self.customer else self.customer_name_backup} on {self.service_date}"
        return f"Special - {self.client_name} on {self.service_date}"
    