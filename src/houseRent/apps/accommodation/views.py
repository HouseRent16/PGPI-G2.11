from .forms import RegisterAccommodation, RegisterImage, ClaimForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from apps.authentication.forms import RegisterAddress
from apps.core.models import Accommodation, Address, CustomUser, Claim, Image


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

            # Obtener el ID del alojamiento recién creado
            accommodation_id = accommodation.id
            
            messages.success(request, 'Alojamiento registrado correctamente')

            # Construir la URL de redirección utilizando reverse
            redirect_url = reverse('registerImage', args=[accommodation_id])

            return redirect(redirect_url)
    else:
        formAccommodation = RegisterAccommodation()
        formAddress = RegisterAddress()
        
   
    return render(request, 'accommodation/add.html', {'formAccommodation': formAccommodation,'formAddress': formAddress})

def register_image(request, accommodation_id):
    if request.method == 'POST':
        formImage = RegisterImage(request.POST, request.FILES)
        if formImage.is_valid():
            image = formImage.save(commit=False)
            image.accommodation_id = accommodation_id
            image.save()
            messages.success(request, 'Alojamiento registrado correctamente')
            return redirect('gestion')
    else:
        formImage = RegisterImage()
    
    return render(request, 'accommodation/addImage.html', {'formImage': formImage})


def claim_list(request):
    user_accommodations = Accommodation.objects.filter(owner=request.user.id)
    claims = Claim.objects.filter(accommodation__in=user_accommodations)
    return render(request, 'accommodation/claim_list.html', {'claims': claims})

def claim_details(request, claim_id):
    # Obtener la reclamación específica o devolver un error 404 si no existe
    claim = get_object_or_404(Claim, id=claim_id)
    return render(request, 'accommodation/claim_details.html', {'claim': claim})

def claimRespond(request,claim_id):
    claim= get_object_or_404(Claim,id=claim_id)
    if request.method=='POST':
        form= ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('/claims')
    else:
        form=ClaimForm(instance=claim)
    return render(request,'accommodation/claimResponseForm.html',{'form':form})
        

