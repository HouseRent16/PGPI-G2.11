from django.urls import path
from .views import request_booking, CreateCheckoutSessionView
from apps.booking import views

urlpatterns = [
    path('<int:accommodation_id>', request_booking, name='request_booking'),
    path('owner',views.books,name='booking'),
    path('owner/<int:ID>',views.detailsBooks, name='detailsBooking'),
    path('create-checkout-session/<int:book_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', views.paymentSuccessView, name='payment-success'),
    path('cancel/', views.paymentCancelView, name='payment-cancel'),
    path('createStripeAccount', views.create_stripe_account_for_owner,name='create_stripe_account'),

]