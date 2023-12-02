from django.urls import path
from apps.accommodation import views

urlpatterns = [
    path('accommodation/add', views.register_acommodation, name='registerAccommodation'),
    path('claims/', views.claim_list, name='claim_list') 
]
