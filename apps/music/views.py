from django.shortcuts import render, redirect

from . import models


def audio_view(request, slug):
    song = models.Audio.objects.get(slug=slug)
    context = {
        'song': song
    }
    return render(request, 'music/audio_view.html', context)


def audio_compilation_view(request, slug):
    compilation = models.AudioCompilation.objects.get(slug=slug)
    tracks = compilation.tracks
    context = {
        'compilation': compilation,
        'tracks': tracks
    }
    return render(request, 'music/audio_compilation_view.html', context)
