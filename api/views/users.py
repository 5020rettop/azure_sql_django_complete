from rest_framework import generics, response, status
from django.contrib.auth.models import User
from ..serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    # API view to list and create users
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    # API view to retrieve, update or delete a user instance
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteAll(generics.DestroyAPIView):
    # API view to delete all users
    def delete(self, request, *args, **kwargs):
        # Exclude superusers if necessary, but request says "all"
        User.objects.all().delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
