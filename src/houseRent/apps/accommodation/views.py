from .forms import RegisterAccommodation
from django.shortcuts import render, redirect
from apps.authentication.forms import RegisterAddress
from apps.core.models import Accommodation, Address, CustomUser, Claim

from django.contrib import messages

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
    claims = Claim.objects.all()
    return render(request, 'accommodation/claim_list.html', {'claims': claims})

