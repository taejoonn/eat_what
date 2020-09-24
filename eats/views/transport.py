from django.shortcuts import render
from django.http import HttpResponse

def transport(request):
    context = {
        'info': 'How will you get there?',
    }

    return render(request, 'eats/transport.html', context=context)

def travel(request):
    context = {
        'info:': 'How far will you go?'
    }

    return render(request, 'eats/travel.html', context=context)