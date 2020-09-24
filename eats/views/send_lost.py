from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail

def lost_user(request):
    return render(request, 'registration/lost_user.html')

def send_user(request):
    # send email to user's email with password
    email = request.POST.get('email')
    
    ''' check db for a user with this email '''
    try:
        user = User.objects.get(email=email)
    except:
        context = {
            'signal': 400
        }
        return render(request, 'registration/lost_user.html', context)

    send_mail(
        'Username Recovery',
        'Your username is: \n\t\t' + str(user.username),
        'taejoonn@gmail.com',
        [email]
    )

    return HttpResponse('Email Sent!')


def lost_pass(request):
    return render(request, 'registration/password_reset.html')

def send_pass(request):
    # send email to user's email with username
    username = request.POST.get('username')

    ''' check db for a user with this username '''
    try:
        user = User.objects.get(username=username)
    except:
        context = {
            'signal': 400
        }
        return render(request, 'registration/pass_reset.html', context)

    send_mail(
        'Password Recovery',
        'Follow the link to reset your password: \n\t\t' ,
        'taejoonn@gmail.com',
        [user.email]
    )

    return render(request, 'registration/reset_success.html')