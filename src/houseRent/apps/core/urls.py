from django.urls import path
from apps.core import views

urlpatterns = [
    path('admin/core/customuser/<int:user_id>/password/', views.change_password, name='admin_change_password'),
    path('',views.home,name='home'),
    path('api/togglefavorites/', views.togglefavorites, name='togglefavorites'),
    path('accommodation/<accommodation_id>/', views.accommodation_details, name='accommodation-detail'),
    path('api/togglefavorites/', views.togglefavorites, name='togglefavorites'),
    path('sobre-nosotros/', views.sobreNosotros, name="sobreNosotros"),
    path('privatePolicy/', views.private_policy, name="privatePolicy"),
    path('ayuda/', views.ayuda, name="ayuda"),

]