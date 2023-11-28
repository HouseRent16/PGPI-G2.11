from django.urls import path
from apps.books import views

urlpatterns =[
    path('',views.books,name='books'),
    path('<int:ID>',views.detailsBooks, name='detailsBooks')
]