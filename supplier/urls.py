from django.urls import path, include
from rest_framework import routers
from .views import SupplierViewSet, create_supplier, get_suppliers, SupplierUserList, delete_supplier, LoginAPIView,LogoutAPIView

router = routers.DefaultRouter()
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('create/', create_supplier, name='create_supplier'),
    path('suppliers/', get_suppliers, name='supplier_list'),
    path('register/', SupplierUserList.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('supplier/<int:pk>/', delete_supplier, name='delete_supplier'),
    path('', include(router.urls)),
]


#class SortingProducts{
# int pirce,
# String[] sorting;
# String name;
# String category;
#  ArrayList<> listofProducts= new List(["Apple", "b", "", "", "", "", "", ""])
#
#
#
# }