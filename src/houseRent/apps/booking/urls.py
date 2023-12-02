from django.urls import path
from .views import request_booking, booking_history

urlpatterns = [
    path('<int:accommodation_id>', request_booking, name='request_booking'),
    path('history', booking_history, name='history'),
   
]