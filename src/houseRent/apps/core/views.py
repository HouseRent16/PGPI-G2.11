import json
from unittest import case
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Accommodation, Favorite, Service, Image, Book, Comment, Claim, Address
from .enums import Category, BookingStatus
from .forms import AdminPasswordChangeForm, CommentForm, ClaimForm
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime, date
from urllib.parse import urlencode
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.db.models import Q, Exists, OuterRef, Value, BooleanField, Avg, F
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from .forms import CustomUserForm, AddressForm
from django.shortcuts import get_object_or_404


@staff_member_required
def change_password(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('admin:index')
    else:
        form = AdminPasswordChangeForm(user)
    return render(request, 'core/change_password.html', {
        'form': form
    })

def home(request):
    accommodations = Accommodation.objects.all().annotate(
        is_booked=Value(False, output_field=BooleanField()),
        is_favorite=Value(False, output_field=BooleanField())
    )

    if request.user.is_authenticated:
        # Obtén los los alojamientos favoritos del usuario actual
        favorite = Favorite.objects.filter(accommodation=OuterRef('pk'), user=request.user)
        # Actualiza el campo is_favorite a True para los alojamientos favoritos
        accommodations = accommodations.annotate(
            is_favorite=Exists(favorite)
        )


    # Filtros
    name_query = request.GET.get('name')
    owner_query = request.GET.get('owner')
    type_query = request.GET.get('type')
    min_capacity = request.GET.get('min_capacity')
    max_capacity = request.GET.get('max_capacity')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country_query = request.GET.get('country')
    region_query = request.GET.get('region')
    city_query = request.GET.get('city')
    postal_code_query = request.GET.get('pcode')
    services_query = request.GET.getlist('services')
    min_rating = request.GET.get('min_rating')

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
    except ValueError:
        start_date = None
    try:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        end_date = None
    try:
        min_capacity = int(min_capacity) if min_capacity else None
    except ValueError:
        min_capacity = None
    try:
        max_capacity = int(max_capacity) if max_capacity else None
    except ValueError:
        max_capacity = None
    try:
        min_price = float(min_price) if min_price else None
    except ValueError:
        min_price = None
    try:
        max_price = float(max_price) if max_price else None
    except ValueError:
        max_price = None

    if start_date and end_date and start_date > end_date:
        end_date = None
    if min_capacity and max_capacity and min_capacity > max_capacity:
        max_capacity = None
    if min_price and max_price and min_price > max_price:
        max_price = None

    valid_query_params = {
        'name': name_query or '',
        'owner': owner_query or '',
        'type': type_query or '',
        'min_capacity': min_capacity if min_capacity is not None else '',
        'max_capacity': max_capacity if max_capacity is not None else '',
        'min_price': min_price if min_price is not None else '',
        'max_price': max_price if max_price is not None else '',
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'country': country_query or '',
        'region': region_query or '',
        'city': city_query or '',
        'pcode': postal_code_query or '',
        'min_rating': min_rating if min_rating is not None else '',
        'services': services_query  # Mantén services como una lista
    }

    valid_query_string = urlencode(valid_query_params, doseq=True)

    current_query_string = request.GET.urlencode()
    if current_query_string != valid_query_string:
        return HttpResponseRedirect(f'{request.path}?{valid_query_string}')

    if name_query:
        accommodations = accommodations.filter(name__icontains=name_query)
    if owner_query:
        accommodations = accommodations.filter(owner__username__icontains=owner_query)
    if type_query:
        accommodations = accommodations.filter(category=Category.get_readable_name(type_query))
    if min_capacity:
        accommodations = accommodations.filter(capacity__gte=min_capacity)
    if max_capacity:
        accommodations = accommodations.filter(capacity__lte=max_capacity)
    if min_price:
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price:
        accommodations = accommodations.filter(price__lte=max_price)
    if country_query:
        accommodations = accommodations.filter(address__country__icontains=country_query)
    if region_query:
        accommodations = accommodations.filter(address__region__icontains=region_query)
    if city_query:
        accommodations = accommodations.filter(address__city__icontains=city_query)
    if postal_code_query:
        accommodations = accommodations.filter(address__postal_code__icontains=postal_code_query)

    if start_date and end_date:
    # Encuentra reservas que se solapen con el rango de fechas
        overlapping_books = Book.objects.filter(
            accommodation=OuterRef('pk'),
            start_date__lt=end_date,
            end_date__gt=start_date,
            is_active=True
        )
        accommodations = accommodations.annotate(
            is_booked=Exists(overlapping_books)
        )

    if services_query:
        accommodations = accommodations.filter(service__id__in=services_query).distinct()
    if min_rating:
        accommodations = [accommodation for accommodation in accommodations if (accommodation.average_rating or 0) >= float(min_rating)]

    for accommodation in accommodations:
        accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()
        
    es_propietario=request.user.groups.filter(name="Propietarios").exists()

    tipos = Category.choices()
    servicios = Service.objects.all()

    context = {
        'accommodations': accommodations,
        'types': tipos,
        'services': servicios,
        'today': date.today(),
    }

    return render(request, 'core/home.html', context)

@login_required
def togglefavorites(request):
    if request.method == 'POST':
        # Obtener el ID del alojamiento desde la solicitud POST
        data = json.loads(request.body)
        accommodation_id = data.get('accommodationId')
        # Obtener el id del usuario actual
        user_id = CustomUser.objects.get(id=request.user.id).id

        class_selected = data.get('classSelected')

        #Verificar la classe del botón para añadir o eliminar a favoritos
        if class_selected == False:
            # Verificar si ya existe la entrada en favoritos para evitar duplicados
            if not Favorite.objects.filter(user_id=user_id, accommodation_id=accommodation_id).exists():
                Favorite.objects.create(user_id=user_id, accommodation_id=accommodation_id)

            return JsonResponse({'status': 'success'})
        else:
            # Eliminar la entrada de favoritos
            if Favorite.objects.filter(user_id=user_id, accommodation_id=accommodation_id).exists():
                Favorite.objects.filter(user_id=user_id, accommodation_id=accommodation_id).delete()
            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

def favoritos(request):

    user_id = CustomUser.objects.get(id=request.user.id).id
    favoritos = Favorite.objects.filter(user_id=user_id)
    accommodations = Accommodation.objects.filter(favorite__in=favoritos)
    for accommodation in accommodations:
        accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()


    context = {
        'favoritos': favoritos,
        'accommodations': accommodations,
    }

    return render(request, 'core/favoritos.html', context)

def private_policy(request):
    return render(request, 'authentication/privatePolicy.html')
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    
    def get_template(self):
        return 'core/profile.html'
    
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=request.user.id)
        customUserForm = CustomUserForm(instance=user)
        addressForm = AddressForm(instance=user.address)

        context = {
            'user_form': customUserForm,
            'address_form': addressForm,
            
        }
        return render(self.request, self.get_template(), context)
    
    #Por hacer
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            user = CustomUser.objects.get(id=request.user.id)
            address = user.address
            customUserForm = CustomUserForm(request.POST, instance=user)
            addressForm = AddressForm(request.POST, instance=address)
          

            if customUserForm.is_valid() and addressForm.is_valid():
                customUserForm.save()
                addressForm.save()
                
                messages.success(request, 'Usuario actualizado correctamente')
                return redirect('home')
            else:
                print("Form validation errors:")
                print(customUserForm.errors)
                print(addressForm.errors) 
                

        context = {
            'user_form': customUserForm,
            'address_form': addressForm,
        }

        return render(self.request, self.get_template(), context)

def ayuda(request):
    return render(request,'core/ayuda.html')

def sobreNosotros(request):
    return render(request, 'core/sobre_nosotros.html')


def accommodation_details(request, accommodation_id):
    accommodation = Accommodation.objects.get(pk=accommodation_id)
    images = accommodation.image_set.all()
    imagenInicial=images[0]

    # accommodation = get_object_or_404(Accommodation, pk=accommodation_id)

    context = {
        "accommodation": accommodation,
        'id': accommodation_id,
        'images': images[1:len(images)],
        'imagenInicial': imagenInicial,
        'numFavoritos': conteoFavoritos(request, accommodation_id),
        'rating': ratingAccommodation(request, accommodation_id),
        'claim': conteoReclamaciones(request, accommodation_id),
        'reservas': conteoReservasTotales(request, accommodation_id),
        'comments': Comment.objects.filter(accommodation_id=accommodation_id),
    }

    return render(request, 'accommodation/accommodation_detail.html', context)

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

def conteoReservasTotales(request, id_accommodation):
    reservas=Book.objects.filter(accommodation_id=id_accommodation)
    return reservas.filter(status=BookingStatus.CONFIRMED).count()
@login_required
def add_comment(request, accommodation_id):
    accommodation = Accommodation.objects.get(pk=accommodation_id)

    user_has_booking = Book.objects.filter(user=request.user, accommodation=accommodation).exists()

    if not user_has_booking:
        raise Http404("No puedes dejar un comentario para este apartamento sin haberlo alquilado.")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.accommodation = accommodation
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()


    return render(request, 'comments-claim/add_comment.html', {'form': form, 'accommodation': accommodation})

@login_required
def add_claim(request, booking_id):
    booking = Book.objects.get(pk=booking_id)

    user_has_booking = Book.objects.filter(user=request.user, pk=booking_id).exists()
    if not user_has_booking:
        raise Http404("No puedes dejar una reclamación para este apartamento sin haberlo alquilado.")


    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.user = request.user
            claim.accommodation = booking.accommodation
            claim.save()
            return redirect('home')
    else:
        form = ClaimForm()

    return render(request, 'comments-claim/add_claim.html', {'form': form, 'booking': booking})

