from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from .forms import AdminPasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def change_password(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password1"])
            user.save()
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('admin:index')
    else:
        form = AdminPasswordChangeForm(user)
    return render(request, 'core/change_password.html', {
        'form': form
    })
