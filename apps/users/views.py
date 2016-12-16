from django.http import Http404
from django.shortcuts import render, redirect
from .models import EmailUser


def my_profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'users/my_profile.html', context)


def settings_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'users/settings.html', context)


def profile_view(request, user_id):
    user = EmailUser.objects.get(id=user_id)
    if request.user.id == user.id:
        return redirect('users:me')
    context = {
        'user': user
    }
    return render(request, 'users/profile_page.html', context)
