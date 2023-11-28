from django.shortcuts import render,redirect
from apps.core.models import Accommodation,Book,Image
from datetime import datetime,timezone

def books(request):
     if request.user.is_authenticated:
        accommodations=Accommodation.objects.filter(owner_id=request.user.id)
        books=dict()
        for accommodation in accommodations:
            accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()
            books[accommodation]=Book.objects.filter(accommodation_id=accommodation.id)
        return render(request,'core/books/books.html',{"books": books})
     else:
         return redirect('login')
     
def detailsBooks(request,ID):
    books=Book.objects.filter(accommodation_id=ID)
    timeNow=datetime.now(timezone.utc)
    nextBook=[]
    pastBook=[]
    for book in books:
         if book.end_date > timeNow:
            nextBook.append(book)
         else:
            pastBook.append(book)
    context={
        'nextBooks': nextBook,
        'pastBooks':pastBook,
        'timeNow': timeNow 
    }
    return render(request,'core/books/detailsBooks.html',context)
