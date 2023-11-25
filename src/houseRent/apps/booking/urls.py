from django.urls import path
from .views import request_booking

urlpatterns = [
    path('booking/', request_booking, name='request_booking'),
   
]