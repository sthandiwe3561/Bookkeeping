from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass 

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    estate = models.CharField(max_length=100)
    plot_no = models.IntegerField()

    def __str__(self):
        return self.name
    