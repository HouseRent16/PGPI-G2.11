from django.urls import path
from apps.booking import views

urlpatterns =[
    path('owner',views.books,name='booking'),
    path('owner/<int:ID>',views.detailsBooks, name='detailsBooking')
]