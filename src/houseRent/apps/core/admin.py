from django.contrib import admin
from .models import Address, CustomUser, Accommodation, Image,Service,Comment,Claim,Favorite,Book

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'number', 'city', 'province', 'country', 'zipcode']
    list_filter = ['street', 'number', 'city', 'province', 'country', 'zipcode']
    search_fields = ['street', 'number', 'city', 'province', 'country', 'zipcode']

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'address', 'owner', 'category']
    list_filter = ['name', 'description', 'price', 'address', 'owner', 'category']
    search_fields = ['name', 'description', 'price', 'address', 'owner', 'category']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','image', 'alt', 'accommodation']
    list_filter = ['title','image', 'alt', 'accommodation']
    search_fields = ['title','image', 'alt', 'accommodation']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_staff', 'is_active']
    list_filter = ['username', 'is_staff', 'is_active']
    search_fields = ['username']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', 'description']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','publicationDate','user','rating','accommodation']
    list_filter = ['title', 'description','publicationDate','user','rating','accommodation']
    search_fields = ['title','publicationDate','rating']

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ['title', 'description','publicationDate','user','accommodation']
    list_filter = ['title', 'description','publicationDate','user','accommodation']
    search_fields = ['title','publicationDate']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['date', 'accommodation','client']
    list_filter = ['date', 'accommodation','client']
    search_fields = ['date']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date','paymentMethod','user','amountPeople','price','isActive','accommodation']
    list_filter = ['start_date', 'end_date','paymentMethod','user','amountPeople','price','isActive','accommodation']
    search_fields = ['start_date','end_date','user','amountPeople']