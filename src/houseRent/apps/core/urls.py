from django.urls import path
from apps.core import views

urlpatterns = [
    path('admin/core/customuser/<int:user_id>/password/', views.change_password, name='admin_change_password'),
    path('',views.home,name='home'),
    path('api/togglefavorites/', views.togglefavorites, name='togglefavorites'),
    path('profile/',views.ProfileView.as_view(),name='profile'),

]