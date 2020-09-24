from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def test(request):
    return render(request, 'eats/test.html')