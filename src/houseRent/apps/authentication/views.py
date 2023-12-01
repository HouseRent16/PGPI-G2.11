# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterAccommodation, RegisterUser, RegisterAddress
from django.contrib.auth.views import LoginView

from .forms import LoginForm, GuestLoginForm
from apps.core.models import Accommodation, CustomUser, Address
from django.contrib import messages

from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']


            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Manejar la situación en la que no se encuentra el usuario
                form.add_error(None, 'Usuario con este correo electrónico no encontrado.')
                return render(request, 'authentication/login.html', {'form': form})
            
            user2 = authenticate(request, username=user.username, password=password)
            print("Segundo:",type(user))

            if user2 is not None:
                login(request, user2)
                # Redirigir a la página principal o a la página que desees
                return redirect('home')
            else:
                # Usuario no válido
                # Puedes agregar un mensaje de error en el formulario
                form.add_error(None, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        user = CustomUser()
        address = Address()
        formUser = RegisterUser(request.POST, instance=user)
        formAddress = RegisterAddress(request.POST, instance=address)
        if formUser.is_valid() and formAddress.is_valid():
            user.set_password(formUser.cleaned_data['password'])
            address.save()
            user.address = address
            user.save()
            messages.success(request, 'Usuario registrado correctamente')
            return redirect('login')
           
    else:
        formUser = RegisterUser()
        formAddress = RegisterAddress()

    return render(request, 'authentication/register.html', {'formUser': formUser, 'formAddress': formAddress})

def private_policy(request):
    return render(request, 'authentication/privatePolicy.html')

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
