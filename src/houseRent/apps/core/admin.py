from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from .models import Address, CustomUser, Accommodation, Image,Service,Comment,Claim,Favorite,Book

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['street', 'number', 'city', 'province', 'country', 'zipcode']
    list_filter = ['street', 'number', 'city', 'province', 'country', 'zipcode']
    search_fields = ['street', 'number', 'city', 'province', 'country', 'zipcode']

@admin.register(Accommodation)
class AccommodationAdmin(ModelAdmin):
    list_display = ['name', 'description', 'price', 'address', 'owner', 'category']
    list_filter = ['name', 'description', 'price', 'address', 'owner', 'category']
    search_fields = ['name', 'description', 'price', 'address', 'owner', 'category']

@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = ['title','image', 'alt', 'accommodation']
    list_filter = ['title','image', 'alt', 'accommodation']
    search_fields = ['title','image', 'alt', 'accommodation']

@admin.register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    list_display = ['username', 'is_staff', 'is_active']
    list_filter = ['username', 'is_staff', 'is_active']
    search_fields = ['username']

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_change_password'] = True
        return super(CustomUserAdmin, self).changeform_view(request, object_id, form_url, extra_context)

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['password'].help_text = format_html(
            '<a href="{}">Cambiar contraseña</a>',
            '../password/'
        )
        return super(CustomUserAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = ['name', 'description']
    list_filter = ['name', 'description']
    search_fields = ['name']

@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['title', 'description','publicationDate','user','rating','accommodation']
    list_filter = ['title', 'description','publicationDate','user','rating','accommodation']
    search_fields = ['title','publicationDate','rating']

@admin.register(Claim)
class ClaimAdmin(ModelAdmin):
    list_display = ['title', 'description','publicationDate','user','accommodation']
    list_filter = ['title', 'description','publicationDate','user','accommodation']
    search_fields = ['title','publicationDate']

@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ['date', 'accommodation','client']
    list_filter = ['date', 'accommodation','client']
    search_fields = ['date']

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['start_date', 'end_date','paymentMethod','user','amountPeople','isActive','accommodation']
    list_filter = ['start_date', 'end_date','paymentMethod','user','amountPeople','isActive','accommodation']
    search_fields = ['start_date','end_date','user','amountPeople']