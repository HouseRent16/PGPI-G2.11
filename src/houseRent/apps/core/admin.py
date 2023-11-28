from django.contrib import admin
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from .models import Address, CustomUser, Accommodation, Image,Comment,Claim,Favorite,Book
from .enums import Request

def add_to_owners(modeladmin, request, queryset):
    owners_group = Group.objects.get(name='Propietarios')
    for user in queryset:
        user.groups.add(owners_group)
        user.request = Request.ACCEPTED.name
        user.save()

add_to_owners.short_description = "Añadir como propietario"

@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ['street_number', 'address_line', 'city', 'region', 'country', 'postal_code']
    list_filter = ['street_number', 'address_line', 'city', 'region', 'country', 'postal_code']
    search_fields = ['street_number', 'address_line', 'city', 'region', 'country', 'postal_code']

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

    actions = [add_to_owners]

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


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display = ['title', 'description','publication_date','user','rating','accommodation']
    list_filter = ['title', 'description','publication_date','user','rating','accommodation']
    search_fields = ['title','publication_date','rating']

@admin.register(Claim)
class ClaimAdmin(ModelAdmin):
    list_display = ['title', 'description','publication_date','user','accommodation']
    list_filter = ['title', 'description','publication_date','user','accommodation']
    search_fields = ['title','publication_date']

@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ['date', 'accommodation','user']
    list_filter = ['date', 'accommodation','user']
    search_fields = ['date']

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ['start_date', 'end_date','payment_method','user','amount_people','is_active','accommodation']
    list_filter = ['start_date', 'end_date','payment_method','user','amount_people','is_active','accommodation']
    search_fields = ['start_date','end_date','user','amount_people']