from django.shortcuts import render,redirect,get_object_or_404
from apps.core.models import Accommodation,Book,Image, Service, Favorite, Comment,Claim,Image,CustomUser
from datetime import datetime,timezone
from .forms import BookingRequest, UserBookRequest
from apps.core.enums import BookingStatus
from django.forms.models import model_to_dict
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.views import View
from django.http import HttpResponse

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
            return redirect('/')
    else:
         return redirect('login')
     
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
                'propietario': es_propietario

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



# Create your views here.


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
            return redirect('/')
        else: 
            return render(request, 'booking/book.html', {'form': form, 'user_form': user_form,  "accommodation":accommodation})
        
##pasarela de pago del cliente


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    @login_required(login_url='login')
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
                success_url=request.build_absolute_uri('/success/'),  # URL de redirección después del pago exitoso
                cancel_url=request.build_absolute_uri('/cancel/'),  # URL de redirección si el usuario cancela
            )

            # Redirige al usuario a la página de pago de Stripe
            return redirect(session.url, code=303)

        except Exception as e:
            # Manejar excepciones o errores aquí
            return HttpResponse(str(e))
def paymentSuccessView(request):
    return render(request,'booking/paymentSuccess.html')

def paymentCancelView(request):
    return render(request,'booking/paymentCancel.html')

#gestion pasarela de pago para el propietario
@login_required(login_url='login')
def create_stripe_account_for_owner(request):
    user=CustomUser.objects.get(request.user.id)
    account = stripe.Account.create(
        type="express",  # o "standard", dependiendo de tus necesidades
        country="ES",  # Asegúrate de usar el país adecuado
        email=user.email
    )
    user.stripe_id=account.id
    user.save()
    return account
    
    
def generate_onboarding_link(stripe_account_id):
    link = stripe.AccountLink.create(
        account=stripe_account_id,
        refresh_url="https://createStripeAccount",
        return_url="https://your-site.com/return",
        type="account_onboarding",
    )
    return link.url
    
def transfer_funds_to_owner(stripe_account_id, amount):
    transfer = stripe.Transfer.create(
        amount=amount,
        currency="eur",
        destination=stripe_account_id,
    )
    return transfer