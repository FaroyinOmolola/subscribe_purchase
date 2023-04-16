from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from accounts.serializers import UserSerializer
from .models import Payment, PaymentCard, Purchase


class PaymentMethodSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PaymentCard
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


def next_payment_date(frequency):
    today = timezone.now()
    if frequency == "weekly":
        next_payment_date = today + timedelta(weeks=1)
    elif frequency == "monthly":
        next_payment_date = today + timedelta(weeks=4)
    elif frequency == "yearly":
        next_payment_date = today + timedelta(weeks=52)
    elif frequency == "daily":
        next_payment_date = timezone.now() + timedelta(days=1)
    elif frequency == "hourly":
        next_payment_date = timezone.now() + timedelta(hours=1)
    elif frequency == "minutely":
        next_payment_date = timezone.now() + timedelta(minutes=1)
    return next_payment_date
