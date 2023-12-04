from django.shortcuts import render,redirect,get_object_or_404
from apps.core.models import Accommodation,Book,Image, Service, Favorite, Comment,Claim,Image,CustomUser
from datetime import datetime,timezone
from .forms import BookingRequest, UserBookRequest
from apps.core.enums import BookingStatus
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from utils.mailer import send_mail
from datetime import datetime

from django.db.models import Q
from apps.core.models import Book, Image
from apps.core.enums import BookingStatus
from django.urls import reverse

from ..core.enums import BookingStatus
from apps.core.views import conteoReservasTotales, conteoFavoritos, ratingAccommodation, conteoReclamaciones

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
def books(request):
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
            return redirect('')
    else:
         return redirect('login')

@login_required    
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
            return redirect('')
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
            booking_request.save()
            str_start_date = booking_request.start_date.strftime("%d/%m/%Y")
            str_end_date = booking_request.end_date.strftime("%d/%m/%Y")
            nights = (booking_request.end_date - booking_request.start_date)
            price = (nights.days - 1 )* accommodation.price
            body = "Su reserva para {} ha sido confirmada, para las fechas {} - {}. Por cun coste de {}€".format(accommodation.name, str_start_date, str_end_date, price)
            send_mail("Información de reserva", body, [user_form.cleaned_data.get("email")],"mailer/email_booking.html", {"code": booking_request.code, "addres": accommodation.address})
            return redirect('/')
        else: 
            return render(request, 'booking/book.html', {'form': form, 'user_form': user_form,  "accommodation":accommodation})
        
def booking_details(request):

    code = request.GET.get('code')

    context = {}

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
        }
    
    return render(request, 'booking/bookingDetails.html', context)

@login_required
def booking_history(request):
    current_user = request.user

    pendding_booking = Book.objects.filter(Q(user=current_user) & Q(is_active=False) & ~Q(status=BookingStatus.CANCELLED)).order_by('start_date')
    confirm_booking = Book.objects.filter(Q(user=current_user) & Q(is_active=True) & ~Q(status=BookingStatus.CANCELLED)).order_by('start_date')
    cancel_booking = Book.objects.filter(Q(user=current_user) & Q(is_active=False) & Q(status=BookingStatus.CANCELLED)).order_by('start_date')

    for booking in pendding_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()
    for booking in confirm_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()
    for booking in cancel_booking:
        booking.accommodation.first_image = Image.objects.filter(accommodation=booking.accommodation, order=1).first()

    """
    judge_url = request.get_host() + reverse('judge')
    claim_url = request.get_host() + reverse('claim')
    cancel_url = request.get_host() + reverse('cancel')
    """

    return render(request, 'booking/history.html', {'pendding_booking': pendding_booking, 'confirm_booking': confirm_booking, 'cancel_booking': cancel_booking}) #, 'judge_url': judge_url, 'claim_url':claim_url , 'cancel_url': cancel_url})


def conteoReservasTotales(request, id_accommodation):
    reservas=Book.objects.filter(accommodation_id=id_accommodation)
    return reservas.filter(status=BookingStatus.CONFIRMED).count()

        
#----------cancelar reservas de un usuario-------

@login_required
@require_POST
def cancelBooksUser(request,book_id):
    if request.user.is_authenticated:
        book=Book.objects.get(id=book_id)
        book.is_active=False
        book.status=BookingStatus.CANCELLED
        book.save()
    return redirect('/booking/history')