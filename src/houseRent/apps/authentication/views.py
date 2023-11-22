# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import RegisterUser, RegisterAddress
from django.contrib.auth.views import LoginView

from .forms import LoginForm, GuestLoginForm

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
        formUser = RegisterUser(request.POST)
        formAddress = RegisterAddress(request.POST)
        if formUser.is_valid() and formAddress.is_valid():
            address = formAddress.save()
            user = formUser.save(commit=False)
            user.address = address
            user.save()

            return redirect('login')
           
    else:
        formUser = RegisterUser()
        formAddress = RegisterAddress()

    return render(request, 'authentication/register.html', {'formUser': formUser, 'formAddress': formAddress})

class GuestLoginView(LoginView):
    template_name = 'login.html'
    form_class = GuestLoginForm

    def form_valid(self, form):
        # Añade la lógica de acceso como invitado aquí
        return super().form_valid(form)

