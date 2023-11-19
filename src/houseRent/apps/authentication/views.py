# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirigir a la página principal o a la página que desees
                return redirect('home')
            else:
                # Usuario no válido
                # Puedes agregar un mensaje de error en el formulario
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.set_password(form.cleaned_data['password'])    # Encriptar contraseña
            user_form.save()
            # Redirigir a la página principal o a la página que desees
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            form.add_error(None, 'datos incorrectos.')
    else:
        form = CustomUserCreationForm()


    return render(request, 'authentication/register.html', {'form': form})
