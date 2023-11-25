from django.shortcuts import render, redirect
from apps.core.models  import Accommodation
from django.shortcuts import get_object_or_404
from .forms import BookingRequest, UserBookRequest
from django.forms.models import model_to_dict

# Create your views here.


def request_booking(request):
    #accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    current_user = request.user
    user_dict = model_to_dict(current_user)
    if not current_user.is_authenticated:
        user_form = UserBookRequest()
    else:
        user_form = UserBookRequest(instance=current_user)
    if request.method == 'GET':
        form = BookingRequest()
        return render(request, 'booking/book.html', {'form': form, 'current_user': current_user, 'user_form': user_form})
    else:
        form = BookingRequest(request.POST)
        if form.is_valid():
            #Proyect.objects.create(name=request.POST['name'], description=request.POST['description'])
            return redirect('/home')
        else: 
            return render(request, 'booking/book.html', {'form': form, 'current_user': current_user, 'user_form': user_form})