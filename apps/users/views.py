from django.contrib.auth import logout
from django.http import Http404
from django.shortcuts import render, redirect
from .models import EmailUser


def register_view(request):
    context = {
    }
    return render(request, 'users/register.html', context)


def my_profile(request):
    if request.user.id is None:
        return redirect('board:unpermitted')
    context = {
    }
    return render(request, 'users/my_profile.html', context)


def settings_view(request):
    context = {
    }
    return render(request, 'users/settings.html', context)


def profile_view(request, username):
    user = EmailUser.objects.get(username=username)
    if request.user.id == user.id:
        return redirect('users:me')
    context = {
        'profile': user
    }
    return render(request, 'users/profile_page.html', context)
