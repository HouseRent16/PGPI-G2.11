from django.urls import path
from apps.authentication import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_user, name='register'),
    path('login/privatePolicy', views.private_policy, name='privatePolicy'),
    path('accommodation/add', views.register_acommodation, name='registerAccommodation') 
]
