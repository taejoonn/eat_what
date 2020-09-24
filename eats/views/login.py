from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

""" redirect to html page for registration """
def register(request):
    return render(request, 'registration/register.html')

""" get post forms and save new user"""
def create(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = User.objects.create_user(username, email, password)
    user.save()

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)