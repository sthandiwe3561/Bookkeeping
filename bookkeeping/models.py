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
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_no = models.CharField(max_length=15)
    estate = models.CharField(max_length=100)
    plot_no = models.IntegerField()

    def __str__(self):
        return self.name
    