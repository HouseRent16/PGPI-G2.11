from django.urls import path
from .views import request_booking, booking_history,CreateCheckoutSessionView
from apps.booking import views

urlpatterns = [
    path('', views.booking_details, name='booking'),
    path('<int:accommodation_id>', request_booking, name='request_booking'),
    path('owner',views.books,name='gestion'),
    path('owner/<int:ID>',views.detailsBooks, name='detailsBooking'),
    path('create-checkout-session/<int:book_id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/<int:book_id>', views.paymentSuccessView, name='payment-success'),
    path('cancelPayment/<int:book_id>', views.paymentCancelView, name='payment-cancel'),
    path('createStripeAccount', views.create_stripe_account_for_owner,name='create_stripe_account'),
    path('history', booking_history, name='history'),
    path('cancelBooks/<int:book_id>',views.cancelBooksUser,name='cancelBooksUser'),
    path('acceptPayment/<int:book_id>', views.paymentAccept, name='paymentAccept'),
    
]
