from django.urls import path, include
from .views import BotView
from .router import router

urlpatterns = [
    path('product/',include(router.urls)),
    path("", BotView.as_view())
]