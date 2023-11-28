from django.shortcuts import render, redirect
from apps.core.models  import Accommodation, CustomUser
from django.shortcuts import get_object_or_404
from .forms import BookingRequest, UserBookRequest
from django.forms.models import model_to_dict
from django.db.models import Q

# Create your views here.


def request_booking(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    current_user = request.user
    if not current_user.is_authenticated:
        user_form = UserBookRequest()
    else:
        user_form = UserBookRequest(instance=current_user)


    if request.method == 'GET':
        form = BookingRequest(initial={'accommodation': accommodation})
        form.accommodation = accommodation
        return render(request, 'booking/book.html', {'form': form, 'user_form': user_form, "accommodation":accommodation})
    else:
        form = BookingRequest(request.POST, initial={'accommodation': accommodation})
        form.accommodation = accommodation
        if not current_user.is_authenticated:
            user_form = UserBookRequest(request.POST)
            if CustomUser.objects.filter(email=user_form.data.get('email')).exists():
                current_user = CustomUser.objects.filter(Q(email=user_form.data.get('email'))).first()
                user_form = UserBookRequest(request.POST, instance=current_user)
        else:
            user_form = UserBookRequest(request.POST, instance=current_user)

        if form.is_valid() and user_form.is_valid():

            booking_request = form.save(commit=False)
            user_loaded = user_form.save()
            booking_request.user = user_loaded
            booking_request.is_active = True
            booking_request.accommodation = accommodation
            booking_request.save()
            return redirect('/')
        else: 
            return render(request, 'booking/book.html', {'form': form, 'user_form': user_form,  "accommodation":accommodation})