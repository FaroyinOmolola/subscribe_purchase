from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from purchases.views import PaymentCardViewSet, PurchaseViewSet
from products.views import ProductViewSet
from accounts.views import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"products", ProductViewSet)
router.register(r"payment-card", PaymentCardViewSet)
router.register(r"purchase", PurchaseViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
