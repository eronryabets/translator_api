from django.urls import path, include
from rest_framework import routers
from .views import TranslatorViewSet

router = routers.DefaultRouter()
router.register(r'translate', TranslatorViewSet, basename='translate')

urlpatterns = [
    path('', include(router.urls)),
]
