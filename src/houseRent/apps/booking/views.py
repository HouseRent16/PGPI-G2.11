from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST

from apps.core.enums import BookingStatus
from apps.core.models import Accommodation, CustomUser, Book, Image, Favorite, Comment, Claim
from apps.core.views import (
    conteoReservasTotales,
    conteoFavoritos,
    ratingAccommodation,
    conteoReclamaciones,
)
from .forms import BookingRequest, UserBookRequest
from utils.mailer import send_mail

import stripe


@login_required(login_url="/login/")
def books(request):
    context={}
    if request.user.is_authenticated:
        es_propietario=request.user.groups.filter(name="Propietarios").exists()
        if es_propietario: 
            accommodations=Accommodation.objects.filter(owner_id=request.user.id)
            books=dict()
            for accommodation in accommodations:
                accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()
                books[accommodation]=len(Book.objects.filter(accommodation_id=accommodation.id,is_active=True))
                context={
                    "books": books,
                    'propietario': es_propietario

                }
            return render(request,'booking/booksOwner.html',context)
        else:
            return redirect('/')
    else:
         return redirect('login')

@login_required(login_url="/login/")
def detailsBooks(request,ID):
    if request.user.is_authenticated:
        es_propietario=request.user.groups.filter(name="Propietarios").exists()
        if es_propietario:
            accommodations=Accommodation.objects.filter(id=ID) 
            books=Book.objects.filter(accommodation_id=ID)
            services=accommodations[0].service.all()
            timeNow=datetime.now(timezone.utc)
            nextBook=[]
            pastBook=[]
            cancelBook=[]
            for book in books:
                if book.end_date > timeNow and book.is_active==True:
                    nextBook.append(book)
                elif book.end_date > timeNow and book.is_active==False :
                     cancelBook.append(book)
                else:
                    pastBook.append(book)
            imagenInicial=accomodationImages(request,ID)[0]
            context={
                'nextBooks': sorted(nextBook,key=lambda x: x.id,reverse=True),
                'pastBooks':sorted(pastBook,key=lambda x: x.id,reverse=True),
                'cancelBooks': sorted(cancelBook,key=lambda x: x.id,reverse=True),
                'accommodations':accommodations,
                'accommodation': accommodations[0],
                'services':services,
                'numFavoritos': conteoFavoritos(request,ID),
                'rating': ratingAccommodation(request,ID),
                'claim': conteoReclamaciones(request,ID),
                'imagenInicial': imagenInicial,
                'images': accomodationImages(request,ID)[1:len(accomodationImages(request,ID))],
                'propietario': es_propietario,
                'reservas': conteoReservasTotales(request, ID),

            }
            
            return render(request,'booking/detailsBooksOwner.html',context)
        else:
            return redirect('/')
    else: 
        return redirect('login')

def conteoFavoritos(request,id_accommodation):
    favoritos=Favorite.objects.filter(accommodation_id=id_accommodation)
    return len(favoritos)

def ratingAccommodation(request,id_accommodation):
    comments=Comment.objects.filter(accommodation_id=id_accommodation)
    sumaRating=0
    mediaRating=0
    for comment in comments:
        sumaRating+=comment.rating
    if len(comments)!=0:
        mediaRating=sumaRating/len(comments)
    return mediaRating

def conteoReclamaciones(request,id_accommodation):
    reclamaciones=Claim.objects.filter(accommodation_id=id_accommodation)
    return len(reclamaciones)

def accomodationImages(request,id_accommodation):
    images=Image.objects.filter(accommodation_id=id_accommodation)
    return images

def request_booking(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    current_user = request.user
    if not current_user.is_authenticated:
        user_form = UserBookRequest()
    else:
        user_form = UserBookRequest(instance=current_user)


    if request.method == 'GET':
        form = BookingRequest(initial={'accommodation': accommodation})
        form.accommodation = accommodation
        return render(request, 'booking/book.html', {'form': form, 'user_form': user_form, "accommodation":accommodation})
    else:
        form = BookingRequest(request.POST, initial={'accommodation': accommodation})
        form.accommodation = accommodation
        if current_user.is_authenticated:
            user_form = UserBookRequest(request.POST, instance=current_user)
        else:
            user_form = UserBookRequest(request.POST)

        if form.is_valid() and user_form.is_valid():

            booking_request = form.save(commit=False)
            if current_user.is_authenticated:
                booking_request.user = current_user
            booking_request.is_active = True
            booking_request.accommodation = accommodation
            booking_request.status = BookingStatus.PENDING
            dias=booking_request.end_date-booking_request.start_date
            price=dias.days*accommodation.price
            booking_request.price=price
            if(booking_request.payment_method== 'ONLINE'):
                booking_request.save()
                return redirect('/booking/create-checkout-session/'+str(booking_request.id))
            else:
                booking_request.save()
                str_start_date = booking_request.start_date.strftime("%d/%m/%Y")
                str_end_date = booking_request.end_date.strftime("%d/%m/%Y")
                nights = (booking_request.end_date - booking_request.start_date)
                price = (nights.days) * accommodation.price
                body = "Su reserva para {} ha sido confirmada, para las fechas {} - {}. Por un coste de {}€".format(accommodation.name, str_start_date, str_end_date, price)
                send_mail("Información de reserva", body, [user_form.cleaned_data.get("email")],"mailer/email_booking.html", {"code": booking_request.code, "addres": accommodation.address})
                return redirect('/')
        else: 
            return render(request, 'booking/book.html', {'form': form, 'user_form': user_form,  "accommodation":accommodation})
        
def booking_details(request):

    code = request.GET.get('code')

    context = {}
    try:
        if code:
            book = get_object_or_404(Book, code=code)
            accommodation = book.accommodation
            images = accommodation.image_set.all()
            imagenInicial = images[0]

            context = {
                'book': book,
                'accommodation': accommodation,
                'images': images[1:len(images)],
                'imagenInicial': imagenInicial,
                'numFavoritos': conteoFavoritos(request, accommodation.id),
                'rating': ratingAccommodation(request, accommodation.id),
                'claim': conteoReclamaciones(request, accommodation.id),
                'reservas': conteoReservasTotales(request, accommodation.id),
                'now': datetime.now().date(),
            }
            return render(request, 'booking/bookingDetails.html', context)
    except:
        redirect('/booking')
    
    return render(request, 'booking/bookingDetails.html', context)
    

@login_required(login_url="/login/")
def booking_history(request):
    current_user = request.user

    pendding_booking = Book.objects.filter(Q(user=current_user) & Q(end_date__lt = datetime.now().date()) & Q(is_active=True) & ~Q(status=BookingStatus.CANCELLED)).order_by('start_date')
    confirm_booking = Book.objects.filter(Q(user=current_user) & Q(end_date__gte = datetime.now().date()) & Q(is_active=True) & ~Q(status=BookingStatus.CANCELLED)).order_by('start_date')
    cancel_booking = Book.objects.filter(Q(user=current_user) & Q(is_active=False) & Q(status=BookingStatus.CANCELLED)).order_by('start_date')
    es_propietario=request.user.groups.filter(name="Propietarios").exists()
    for booking in pendding_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()
    for booking in confirm_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()
    for booking in cancel_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()
    now = datetime.now().date()

    return render(request, 'booking/history.html', {'pendding_booking': pendding_booking, 'confirm_booking': confirm_booking, 'cancel_booking': cancel_booking,'propietario':es_propietario, 'now':now})


def conteoReservasTotales(request, id_accommodation):
    reservas=Book.objects.filter(accommodation_id=id_accommodation)
    return reservas.filter(status=BookingStatus.CONFIRMED).count()

        
##pasarela de pago del cliente


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
   
    def get(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': int(book.price * 100),  # Precio en centavos
                        'product_data': {
                            'name': book.amount_people,
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/booking/success/'+str(book_id)),  # URL de redirección después del pago exitoso
                cancel_url=request.build_absolute_uri('/booking/cancelPayment/'+str(book_id)),  # URL de redirección si el usuario cancela
            )

            # Redirige al usuario a la página de pago de Stripe
            return redirect(session.url, code=303)

        except Exception as e:
            # Manejar excepciones o errores aquí
            return HttpResponse(str(e))
def paymentSuccessView(request,book_id):
    return redirect('/booking/acceptPayment/'+str(book_id))

def paymentAccept(request,book_id):
    book=Book.objects.get(id=book_id)
    book.payment_bool=True
    book.save()
    return redirect('/')

def paymentCancelView(request,book_id):
    book=Book.objects.get(id=book_id)
    book.delete()
    return redirect('/')

#gestion pasarela de pago para el propietario
@login_required(login_url="/login/")
def create_stripe_account_for_owner(request):
    user=CustomUser.objects.get(id=request.user.id)
    print("creando cuenta")
    account = stripe.Account.create(
        country="ES",
        type="custom",
        capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}},
        tos_acceptance={"date": 1609798905, "ip": "8.8.8.8"},
        email=user.email,
        business_type="individual",  # o "company" si es aplicable
        company={
            'name': user.username,  # Nombre de la empresa ficticia
            'phone': 1234,  # Número de teléfono de la empresa
                },
        individual={
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': {
            'postal_code': 1234,
            'country': 'ES',
            },
        },
        business_profile={
            'mcc': '5734',  # Código de categoría de comerciante (MCC) para software
                },
        external_account={
            'object': 'bank_account',
            'country': 'ES',
            'currency': 'eur',
            'account_holder_name': 'Nombre del titular',
            'account_holder_type': 'individual',
            'account_number': 'ES0700120345030000067890',  # Número de cuenta (utiliza un número de prueba)
                },
       
           
    )
    user.stripe_id=account.id
    user.save()
    if user.stripe_id!=None:
        return redirect('/')
    else:
        return redirect('/booking/cancel')

    

        
#----------cancelar reservas de un usuario-------

@login_required(login_url="/login/")
@require_POST
def cancelBooksUser(request,book_id):
    book=Book.objects.get(id=book_id)
    user=CustomUser.objects.get(id=request.user.id)
    if request.user.is_authenticated:
        book.is_active=False
        book.status=BookingStatus.CANCELLED
        book.save()
    str_start_date = book.start_date.strftime("%d/%m/%Y")
    str_end_date = book.end_date.strftime("%d/%m/%Y")
    body = "Su reserva para {} ha sido cancelada. Para los dias {} - {}".format(book.accommodation.name, str_start_date, str_end_date)
    send_mail("Confirmación de cancelación de reserva", body, [user.email],"mailer/email_cancel.html")
    if request.user.groups.filter(name='Propietarios').exists():
        return redirect('/booking/owner')
    return redirect('/booking/history')
