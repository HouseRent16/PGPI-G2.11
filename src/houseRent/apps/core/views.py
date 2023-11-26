from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Accommodation, Service, Image, Book
from .enums import Category
from .forms import AdminPasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render 
from django.db.models import Avg
from datetime import datetime
from datetime import date
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.db.models import Q, Exists, OuterRef, Value, BooleanField

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
    accommodations = Accommodation.objects.all().annotate(average_rating=Avg('comment__rating'))

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

    accommodations = Accommodation.objects.all().annotate(is_booked=Value(False, output_field=BooleanField()))

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
        accommodations = accommodations.filter(average_rating__gte=min_rating)

    for accommodation in accommodations:
        accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()

    tipos = Category.choices()
    servicios = Service.objects.all()

    context = {
        'accommodations': accommodations,
        'types': tipos,
        'services': servicios,
        'today': date.today(),
    }    

    return render(request, 'core/home.html', context)
