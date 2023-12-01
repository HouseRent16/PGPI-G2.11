from django.urls import path
from apps.authentication import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('login/privatePolicy', views.private_policy, name='privatePolicy'),
]
