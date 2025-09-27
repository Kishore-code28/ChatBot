from rest_framework.viewsets import ModelViewSet
from .serializer import Product_Serializer
from .models import Products

class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = Product_Serializer()