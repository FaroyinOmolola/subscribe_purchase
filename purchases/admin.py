from django.contrib import admin

from purchases.models import Payment, PaymentCard, Purchase


# Register your models here.
@admin.register(PaymentCard)
class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ["authorization_code", "user_id"]
    search_fields = ["authorization_code"]


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["user_id", "product_id", "start_date"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["amount", "payment_date"]
