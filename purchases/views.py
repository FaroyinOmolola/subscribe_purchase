import requests
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from .models import Payment, PaymentCard, Purchase
from .serializers import (
    PaymentMethodSerializer,
    PaymentSerializer,
    PurchaseSerializer,
    next_payment_date,
)


class PaymentCardViewSet(viewsets.ModelViewSet):
    """ViewSet for adding cards to be used for purchase and recurrent payments.
    card is added from front the frontend using the paystack payment widget for
    authentication of the card after which the reference_id is send to the backend
    which is then verified with the paystack API, if successful the auth_code will be
    saved in PaymentCard model to be used for purchase and recurrent payments
    """

    queryset = PaymentCard.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # please check and run the frontend folder in this project to use the paystack interface to
        # add card and get a reference id that can be used to test this endpoint
        reference_id = request.data.get("reference_id")
        if not reference_id:
            return Response(
                {"error": "reference_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            response = requests.get(
                f"https://api.paystack.co/transaction/verify/{reference_id}",
                headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
            )
            response.raise_for_status()
            json_data = response.json()
            data = json_data["data"]
            data_to_save = {
                "authorization_code": data["authorization"]["authorization_code"],
                "exp_year": data["authorization"]["exp_year"],
                "exp_month": data["authorization"]["exp_month"],
                "payment_email": data["customer"]["email"],
            }
            serializer = self.get_serializer(data=data_to_save)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(
                {
                    "status": True,
                    "message": "Card Added successfully",
                },
                status=status.HTTP_200_OK,
            )
        except requests.exceptions.HTTPError as e:
            response_data = e.response.json()
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class PurchaseViewSet(viewsets.ModelViewSet):
    """View set purchase a product, need to provide the product reference,
    payment method reference and frequency. product amount is charged on the card immediately
    after which that purchase is save and that payment as well"""

    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request):
        # to make a purchase you need to provide the product reference and the payment method reference
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data["product"]
            frequency = serializer.validated_data["frequency"]
            payment_card = serializer.validated_data["payment_card"]

            try:
                # authourize the payment for the product using paystack
                data = {
                    "authorization_code": payment_card.authorization_code,
                    "email": payment_card.payment_email,
                    "amount": float(product.price) * 100,
                }

                response = requests.post(
                    "https://api.paystack.co/transaction/charge_authorization/",
                    headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
                    data=data,
                )
                response.raise_for_status()

                purchase = serializer.save(
                    user=request.user,
                    last_payment_date=timezone.now(),
                    next_payment_date=next_payment_date(frequency),
                )
                # Create a payment object
                Payment.objects.create(
                    user=request.user, amount=product.price, purchase=purchase
                )

                return Response(
                    {
                        "status": True,
                        "message": "Purchase Successful",
                        "data": PurchaseSerializer(purchase).data,
                    },
                    status=status.HTTP_200_OK,
                )
            except requests.exceptions.HTTPError as e:
                response_data = e.response.json()
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["GET"], url_path="payments")
    def get_payments(self, request, pk=None):
        """action to get all payments history for the purchase of a product"""
        purchase = self.get_object()
        payments = purchase.payments.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="end-payments")
    def end_payment(self, request, pk=None):
        """action to end recurrent payments for a purchase and stop all reductions"""
        purchase = self.get_object()
        purchase.stop_deduction = True
        purchase.end_date = timezone.now()
        purchase.save()
        serializer = self.get_serializer(purchase)
        return Response(serializer.data)
