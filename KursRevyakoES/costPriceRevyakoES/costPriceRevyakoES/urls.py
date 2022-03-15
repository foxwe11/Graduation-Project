"""costPriceRevyakoES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from appRevyakoES.views import *

urlpatterns = [
    path('', include('appRevyakoES.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', UserAPIList.as_view()),
    path('api/users/<int:pk>/', UserAPIDetail.as_view()),
    path('api/products/', ProductAPIList.as_view()),
    path('api/products/<int:pk>/', ProductAPIDetail.as_view()),
    path('api/materials/', MaterialAPIList.as_view()),
    path('api/materials/<int:pk>/', MaterialAPIDetail.as_view()),
    path('api/labors/', LaborAPIList.as_view()),
    path('api/labors/<int:pk>/', LaborAPIDetail.as_view()),
    path('api/amortizations/', AmortizationAPIList.as_view()),
    path('api/amortizations/<int:pk>/', AmortizationAPIDetail.as_view()),
    path('api/invoices/', InvoiceAPIList.as_view()),
    path('api/invoices/<int:pk>/', InvoiceAPIDetail.as_view()),
]
