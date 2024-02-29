from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cars.views import *

router = DefaultRouter()
router.register(r'country', CountryViewSet, basename='country')
router.register(r'manufacture', ManufactureViewSet, basename='manufacture')
router.register(r'car', CarViewSet, basename='car')
router.register(r'commentary', CommentaryViewSet, basename='commentary')
router.register(r'export', ExportViewSet, basename='export')

cars_urlpatterns = [
    path('api/', include(router.urls)),
]
