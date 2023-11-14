from django.contrib import admin
from .models import Address, Accommodation, Image

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
    list_display = ['image', 'alt', 'accommodation']
    list_filter = ['image', 'alt', 'accommodation']
    search_fields = ['image', 'alt', 'accommodation']