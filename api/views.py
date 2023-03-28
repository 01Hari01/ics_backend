import json
import os

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from immunocore.settings import BASE_DIR
from supplier.models import Supplier
from supplier.serializers import SupplierSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]



