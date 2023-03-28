import os
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404

from immunocore.settings import BASE_DIR
from supplier.models import Supplier, SupplierUser
from supplier.serializers import SupplierSerializer, SupplierUserSerializer
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class SupplierUserList(generics.ListCreateAPIView):
    queryset = SupplierUser.objects.all()
    serializer_class = SupplierUserSerializer


class UsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user=SupplierUser.objects.get(username=username)
        if user and user.check_password(password):
            return user

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'username': user.username
            })

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer



@api_view(['DELETE'])
def delete_supplier(request, pk):
    try:
        supplier = Supplier.objects.get(pk=pk)
    except Supplier.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    supplier.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def create_supplier(request):
    data = request.data
    # Combine the fields into a single dictionary
    supplier_data = {
        'name': data.get('name', ''),
        'date_created': data.get('date_created', ''),
        'phone_numbers': data.get('phone_numbers', '')
    }
    # Save the data as a JSON object in the database
    supplier = Supplier.objects.create(supplier=supplier_data)
    return JsonResponse({'id': supplier.id, 'supplier': supplier.supplier}, status=201)

@api_view(['GET'])
def get_suppliers(request):
    suppliers = Supplier.objects.all()
    serializer = SupplierSerializer(suppliers, many=True)
    return JsonResponse(serializer.data, status=status.HTTP_200_OK,safe=False)



DATA_FILE = os.path.join(BASE_DIR, 'suppliers.json')








class ObtainTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


@csrf_exempt
def data_view(request):
    if request.method == 'POST':
        new_data = json.loads(request.body)
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            data.extend(new_data)
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
        data = json.loads(json.dumps(data))
    else:
        with open(DATA_FILE) as file:
            data = json.load(file)
    return JsonResponse(data, safe=False)








