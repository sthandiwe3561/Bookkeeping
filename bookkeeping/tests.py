from django.test import TestCase
from .models import Customer

# Create your tests here.
class CustomerModelTest(TestCase):

    def setUp(self):
        # Create a sample customer before each test
        Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            phone_no="0712345678",
            estate="Green Valley",
            plot_no=25
        )

    def test_customer_creation(self):
        """Test if customer was created correctly"""
        customer = Customer.objects.get(name="John Doe")
        self.assertEqual(customer.email, "john@example.com")
        self.assertEqual(customer.phone_no, "0712345678")
        self.assertEqual(customer.estate, "Green Valley")
        self.assertEqual(customer.plot_no, 25)

    def test_string_representation(self):
        """Test the __str__ method of the Customer model"""
        customer = Customer.objects.get(name="John Doe")
        self.assertEqual(str(customer), "John Doe")