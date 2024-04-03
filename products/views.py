from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from products.models import (
    Product,
    NewUser
)
from products.serializers import (
    NewUserDetailSerializer,
    ProductSerializer
)


class LoginViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = NewUserDetailSerializer

    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                serializer = self.serializer_class(user)
                print(serializer)
                return Response(serializer.data)
            else:
                return Response({'error': 'Invalid credentials'}, status=401)
        else:
            return Response({'error': 'Email and Password Requaired'}, status=400)


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not request.user.is_superuser:
            return Response({"message": "You do not have permission to perform this action."}, status=403)
        if serializer.is_valid():
            serializer.validated_data["owner"] = request.user
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({'error': 'Serializer not valid'}, status=403)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner_id != request.user.id:
            return Response({'error': 'You dont have permissions to update'}, status=403)
        else:
            return super().update(request, *args, **kwargs)