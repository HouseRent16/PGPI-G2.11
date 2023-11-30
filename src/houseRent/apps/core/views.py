from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser, Accommodation, Service, Image
from .forms import AdminPasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render 
from django.db.models import Avg

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
    city_query = request.GET.get('city')

    if name_query:
        accommodations = accommodations.filter(name__icontains=name_query)
    if owner_query:
        accommodations = accommodations.filter(owner__username__icontains=owner_query)
    if type_query:
        accommodations = accommodations.filter(category=type_query)
    if min_capacity:
        accommodations = accommodations.filter(capacity__gte=min_capacity)
    if max_capacity:
        accommodations = accommodations.filter(capacity__lte=max_capacity)
    if min_price:
        accommodations = accommodations.filter(price__gte=min_price)
    if max_price:
        accommodations = accommodations.filter(price__lte=max_price)
    if country_query:
        accommodations = accommodations.filter(address__country=country_query)
    if city_query:
        accommodations = accommodations.filter(address__city__icontains=city_query)
    if start_date and end_date:
        accommodations = accommodations.filter(booking__start_date__lte=start_date, booking__end_date__gte=end_date)

    # Para el filtro de servicios, necesitarás ajustar según cómo estén definidos en tu modelo.
    services_query = request.GET.getlist('services')
    if services_query:
        accommodations = accommodations.filter(service__name__in=services_query).distinct()

    for accommodation in accommodations:
        accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()
    es_propietario=request.user.groups.filter(name="Propietarios").exists()
        
    context = {
        'accommodations': accommodations,
        'propietario': es_propietario
    }
    return render(request, 'core/home.html', context)
