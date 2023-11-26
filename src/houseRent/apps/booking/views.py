from django.shortcuts import render, redirect
from apps.core.models  import Accommodation
from django.shortcuts import get_object_or_404
from .forms import BookingRequest, UserBookRequest2
from django.forms.models import model_to_dict

# Create your views here.


def request_booking(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    current_user = request.user
    user_dict = model_to_dict(current_user)
    if not current_user.is_authenticated:
        user_form = UserBookRequest2()
    else:
        user_form = UserBookRequest2(user_dict)
    if request.method == 'GET':
        form = BookingRequest(initial={'accommodation': accommodation})
        form.accommodation = accommodation
        return render(request, 'booking/book.html', {'form': form, 'current_user': current_user, 'user_form': user_form, "accommodation":accommodation})
    else:
        form = BookingRequest(request.POST)
        form.accommodation = accommodation
        user_form = UserBookRequest2(request.POST)
        if not user_form.is_valid():
            print('userform nor valid')
            errores = user_form.errors.as_data()
            # Imprime los errores a la consola para propósitos de depuración
            print(errores)
        if not form.is_valid():
            print('form nor valid')


        if form.is_valid() and user_form.is_valid():

            booking_request = form.save(commit=False)
            #user_loaded = user_form.save()
            booking_request.user = current_user
            booking_request.is_active = True
            booking_request.accommodation = accommodation
            booking_request.save()
            return redirect('/')
        else: 
            
            print("ha habido un error en el form")
            return render(request, 'booking/book.html', {'form': form, 'current_user': current_user, 'user_form': user_form,  "accommodation":accommodation})