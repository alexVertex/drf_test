"""
URL configuration for ElRosSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from cars.views import *

# router = routers.DefaultRouter()
# router.register(r'cars', CarViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenRefreshView.as_view(), name='token_verify'),

    path('api/cars/list/', CarsViewList.as_view()),
    path('api/cars/create/', CarsViewCreate.as_view()),
    path('api/cars/update/<int:pk>', CarsViewUpdate.as_view()),
    path('api/cars/delete/<int:pk>', CarsViewDelete.as_view()),

    path('api/country/list/', CountryViewList.as_view()),
    path('api/country/create/', CountryViewCreate.as_view()),
    path('api/country/update/<int:pk>', CountryViewUpdate.as_view()),
    path('api/country/delete/<int:pk>', CountryViewDelete.as_view()),

    path('api/manufacture/list/', ManufactureViewList.as_view()),
    path('api/manufacture/create/', ManufactureViewCreate.as_view()),
    path('api/manufacture/update/<int:pk>', ManufactureViewUpdate.as_view()),
    path('api/manufacture/delete/<int:pk>', ManufactureViewDelete.as_view()),

    path('api/commentary/list/', CommentaryViewList.as_view()),
    path('api/commentary/create/', CommentaryViewCreate.as_view()),
    path('api/commentary/update/<int:pk>', CommentaryViewUpdate.as_view()),
    path('api/commentary/delete/<int:pk>', CommentaryViewDelete.as_view()),

    path('api/country/export/', ExportCSVCountries.as_view()),
    path('api/manufacture/export/', ExportCSVManufactures.as_view()),
    path('api/cars/export/', ExportCSVCars.as_view()),
    path('api/commentary/export/', ExportCSVCommentaries.as_view()),
    # path('api/v1/', include(router.urls))
    # path('api/v1/carslist/', CarViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('api/v1/carsModel/<int:pk>', CarViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
