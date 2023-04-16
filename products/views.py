from rest_framework import serializers
from .models import Product
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
