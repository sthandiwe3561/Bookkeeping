from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Customer,Invoice,ServiceRecord
from datetime import date

User = get_user_model()



# Create your tests here.
class CustomerModelTest(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='pass1234')

        # Create a sample customer before each test
        self.customer = Customer.objects.create(
            user=self.user,
            name="John Doe",
            email="john@example.com",
            phone_no="0712345678",
            estate="Green Valley",
        )

    def test_customer_creation(self):
        """Test if customer was created correctly"""
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.phone_no, "0712345678")
        self.assertEqual(self.customer.estate, "Green Valley")

    def test_customer_str_representation(self):
        """Test the __str__ method of the Customer model"""
        self.assertEqual(str(self.customer), "John Doe")

class InvoiceServiceTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='pass1234')

        # Create a customer
        self.customer = Customer.objects.create(user=self.user, name='John Doe')

        # Create invoice
        self.invoice = Invoice.objects.create(
            customer=self.customer,
            total_amount=300.00,
            status='draft',
            created_by=self.user
        )

        # Create service and link to invoice
        self.service = ServiceRecord.objects.create(
            customer=self.customer,
            service_type='normal',
            service_description='Lawn mowing',
            price=150.00,
            service_date=date.today(),
            invoice=self.invoice
        )

    def test_service_is_linked_to_invoice(self):
        self.assertEqual(self.service.invoice, self.invoice)

    def test_invoice_has_correct_service(self):
        services = self.invoice.services.all() #type: ignore
        self.assertIn(self.service, services)

    def test_invoice_deletion_sets_service_invoice_to_null(self):
        self.invoice.delete()
        self.service.refresh_from_db()
        self.assertIsNone(self.service.invoice)

    def test_service_str_representation_normal(self):
        expected_str = f"{self.customer.name} on {self.service.service_date}"
        self.assertEqual(str(self.service), expected_str)

    def test_service_str_representation_special(self):
        special_service = ServiceRecord.objects.create(
        customer=None,
        client_name='Jane Doe',
        service_type='special',
        service_description='Tree trimming',
        price=200.00,
        service_date=date.today(),
        invoice=self.invoice
       )
        expected_str = f"Special - Jane Doe on {special_service.service_date}"
        self.assertEqual(str(special_service), expected_str)
