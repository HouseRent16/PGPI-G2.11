from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.accommodation import views

urlpatterns = [
    path('accommodation/add', views.register_acommodation, name='registerAccommodation'),
    path('accommodation/<int:accommodation_id>/image', views.register_image, name="registerImage"),
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<int:claim_id>/', views.claim_details, name="claim_details"),
    path('claims/<int:claim_id>/claimResponse/',views.claimRespond,name='claimRespond')
]

# Agregar configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)