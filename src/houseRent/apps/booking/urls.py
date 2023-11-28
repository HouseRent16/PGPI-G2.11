from django.urls import path
from .views import request_booking

urlpatterns = [
    path('<int:accommodation_id>', request_booking, name='request_booking'),
   
]