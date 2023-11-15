from django.urls import path
from apps.authentication import views

urlpatterns = [
    path('', views.login_view, name='login')
]