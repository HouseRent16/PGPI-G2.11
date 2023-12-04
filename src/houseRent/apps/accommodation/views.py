from .forms import RegisterAccommodation
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from apps.authentication.forms import RegisterAddress
from apps.core.models import Accommodation, Address, CustomUser, Claim


def register_acommodation(request):
    if request.method == 'POST':
        accommodation = Accommodation()
        address = Address()
        formAccommodation = RegisterAccommodation(request.POST, instance=accommodation)
        formAddress = RegisterAddress(request.POST, instance=address)
        if formAccommodation.is_valid() and formAddress.is_valid():
            address.save()
            accommodation.address = address  
            formAccommodation.instance.owner = CustomUser.objects.get(id=request.user.id)
            # Guarda la instancia del formulario en la base de datos
            formAccommodation.save()
            messages.success(request, 'Alojamiento registrado correctamente')
            return redirect('home')
    else:
        formAccommodation = RegisterAccommodation()
        formAddress = RegisterAddress()
   
    return render(request, 'accommodation/add.html', {'formAccommodation': formAccommodation,'formAddress': formAddress})

def claim_list(request):
    user_accommodations = Accommodation.objects.filter(owner=request.user.id)
    claims = Claim.objects.filter(accommodation__in=user_accommodations)
    return render(request, 'accommodation/claim_list.html', {'claims': claims})

def claim_details(request, claim_id):
    # Obtener la reclamación específica o devolver un error 404 si no existe
    claim = get_object_or_404(Claim, id=claim_id)
    return render(request, 'accommodation/claim_details.html', {'claim': claim})

