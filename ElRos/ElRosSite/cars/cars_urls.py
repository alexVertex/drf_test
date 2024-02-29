from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cars.views import *

router = DefaultRouter()
router.register(r'api/country', CountryViewSet, basename='country')
router.register(r'api/manufacture', ManufactureViewSet, basename='manufacture')
router.register(r'api/car', CarViewSet, basename='car')
router.register(r'api/commentary', CommentaryViewSet, basename='commentary')
router.register(r'api/export', ExportViewSet, basename='export')

cars_urlpatterns = [
    path('', include(router.urls)),
]
