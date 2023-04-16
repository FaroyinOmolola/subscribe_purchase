import uuid
from django.db import models

from accounts.models import User
from products.models import Product


class PaymentCard(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authorization_code = models.CharField(unique=True)
    exp_month = models.CharField()
    exp_year = models.CharField()
    payment_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)


class Purchase(models.Model):
    # note minutely and hourly were just added to promptly test implementation
    frequency_choices = (
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("daily", "Daily"),
        ("hourly", "Hourly"),
        ("minutely", "Minutely"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="purchases"
    )
    frequency = models.CharField(choices=frequency_choices, max_length=10)
    start_date = models.DateTimeField(auto_now_add=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, default=None, blank=True)
    stop_deduction = models.BooleanField(default=False, blank=True)
    payment_card = models.ForeignKey(
        PaymentCard, on_delete=models.CASCADE, related_name="purchases"
    )


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="payments"
    )
