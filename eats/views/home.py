from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def home(request):
    print(settings.BASE_DIR)
    banner = 'Welcome to Eat What! \nDon\'t know what your next meal should be? \n We will decide for you!'
    context = {
        'info': banner,
    }
    
    return render(request, 'eats/home.html', context=context)