from django.urls import path
from apps.authentication import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('login/privatePolicy', views.login_guest, name='privatePolicy'),  
]
