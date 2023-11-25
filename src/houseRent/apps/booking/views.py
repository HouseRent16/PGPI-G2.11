from django.shortcuts import render, redirect
from apps.core.models  import Accommodation
from django.shortcuts import get_object_or_404
from .forms import BookingRequest

# Create your views here.


def request_booking(request):
    #accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    current_user = request.user
    
    if request.method == 'GET':
        form = BookingRequest()
        return render(request, 'booking/book.html', {'form': form})
    else:
        form = BookingRequest(request.POST)
        if form.is_valid():
            print("Es el post")
            #Proyect.objects.create(name=request.POST['name'], description=request.POST['description'])
            return redirect('/home')
        else: 
            print(' else ')
            return render(request, 'booking/book.html', {'form': form})