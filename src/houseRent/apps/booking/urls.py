from django.urls import path
from .views import request_booking
from apps.booking import views

urlpatterns = [
    path('<int:accommodation_id>', request_booking, name='request_booking'),
    path('owner',views.books,name='booking'),
    path('owner/<int:ID>',views.detailsBooks, name='detailsBooking'),

]