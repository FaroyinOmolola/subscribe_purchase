from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import requests

from purchases.models import Payment, Purchase
from purchases.serializers import next_payment_date


def process_recurrent_payments():
    # Get all purchases with next_payment_date less than or equal to current datetime
    purchases = Purchase.objects.filter(next_payment_date__lte=timezone.now())
    for purchase in purchases:
        if not purchase.stop_deduction:
            # Charge the user's card here
            data = {
                "authorization_code": purchase.payment_card.authorization_code,
                "email": purchase.payment_card.payment_email,
                "amount": float(purchase.product.price) * 100,
            }

            response = requests.post(
                "https://api.paystack.co/transaction/charge_authorization/",
                headers={"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"},
                data=data,
            )
            if response.status_code == 200:
                # create payment and update the purchase
                purchase.last_payment_date = timezone.now()
                purchase.next_payment_date = next_payment_date(purchase.frequency)
                purchase.save()
                Payment.objects.create(
                    user=purchase.user, amount=purchase.product.price, purchase=purchase
                )


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_recurrent_payments, "interval", minutes=1)
    scheduler.start()
