from django.shortcuts import render,redirect
from apps.core.models import Accommodation,Book,Image, Service, Favorite, Comment,Claim,Image
from datetime import datetime,timezone

def books(request):
    if request.user.is_authenticated:
        es_propietario=request.user.groups.filter(name="Propietarios").exists()
        if es_propietario: 
            accommodations=Accommodation.objects.filter(owner_id=request.user.id)
            books=dict()
            for accommodation in accommodations:
                accommodation.first_image = Image.objects.filter(accommodation=accommodation, order=1).first()
                books[accommodation]=len(Book.objects.filter(accommodation_id=accommodation.id,is_active=True))
            return render(request,'core/books/books.html',{"books": books})
        else:
            return redirect('/')
    else:
         return redirect('login')
     
def detailsBooks(request,ID):
    if request.user.is_authenticated:
        es_propietario=request.user.groups.filter(name="Propietarios").exists()
        if es_propietario:
            accommodations=Accommodation.objects.filter(id=ID) 
            books=Book.objects.filter(accommodation_id=ID)
            services=accommodations[0].service.all() 
            timeNow=datetime.now(timezone.utc)
            nextBook=[]
            pastBook=[]
            cancelBook=[]
            for book in books:
                if book.end_date > timeNow and book.is_active==True:
                    nextBook.append(book)
                elif book.end_date > timeNow and book.is_active==False :
                     cancelBook.append(book)
                else:
                    pastBook.append(book)
            imagenInicial=accomodationImages(request,ID)[0]
            context={
                'nextBooks': sorted(nextBook,key=lambda x: x.id,reverse=True),
                'pastBooks':sorted(pastBook,key=lambda x: x.id,reverse=True),
                'cancelBooks': sorted(cancelBook,key=lambda x: x.id,reverse=True),
                'accommodations':accommodations,
                'accommodation': accommodations[0],
                'services':services,
                'numFavoritos': conteoFavoritos(request,ID),
                'rating': ratingAccommodation(request,ID),
                'claim': conteoReclamaciones(request,ID),
                'imagenInicial': imagenInicial,
                'images': accomodationImages(request,ID)[1:len(accomodationImages(request,ID))]

            }
            
            return render(request,'core/books/detailsBooks.html',context)
        else:
            return redirect('/')
    else: 
        return redirect('login')

def conteoFavoritos(request,id_accommodation):
    favoritos=Favorite.objects.filter(accommodation_id=id_accommodation)
    return len(favoritos)

def ratingAccommodation(request,id_accommodation):
    comments=Comment.objects.filter(accommodation_id=id_accommodation)
    sumaRating=0
    mediaRating=0
    for comment in comments:
        sumaRating+=comment.rating
    mediaRating=sumaRating/len(comments)
    return mediaRating

def conteoReclamaciones(request,id_accommodation):
    reclamaciones=Claim.objects.filter(accommodation_id=id_accommodation)
    return len(reclamaciones)

def accomodationImages(request,id_accommodation):
    images=Image.objects.filter(accommodation_id=id_accommodation)
    return images
