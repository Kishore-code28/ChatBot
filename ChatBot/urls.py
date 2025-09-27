from django.urls import path, include
from .views import ProductViewSet
from .router import router

urlpatterns = [
    path('product/',include(router.urls))
]