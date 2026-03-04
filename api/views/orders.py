from rest_framework import generics, response, status
from django.contrib.auth.models import User
from ..models import Order
from ..serializers import OrderSerializer

class OrderList(generics.ListCreateAPIView):
    # API view to list and create orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        # Associate the order with the current user or a default user
        # For simplicity in this demo, we'll assign to the first user if no auth
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(user=user)

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update, and delete orders
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDeleteAll(generics.DestroyAPIView):
    # API view to delete all orders
    def delete(self, request, *args, **kwargs):
        Order.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
