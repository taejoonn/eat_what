from django.urls import path, include
from .views import home, transport, spin, result, send_lost, login, test
from django.conf import settings
from django.conf.urls.static import static

# Routes the urls with html pages

urlpatterns = [
    path('', home.home, name='home'),
    path('transport/', transport.transport, name='transport'),
    path('travel/', transport.travel, name="travel"),
    path('spin/', spin.spin, name="spin"),
    path('result/', result.result, name="result"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/lost-pass/', send_lost.lost_pass, name="lost_pass"),
    path('accounts/lost-username/', send_lost.lost_user, name="lost_user"),
    path('accounts/send-pass/', send_lost.send_pass, name="send_pass"),
    path('accounts/send-user/', send_lost.send_user, name="send_user"),
    path('accounts/register/', login.register, name="register"),
    path('accounts/create-user/', login.create, name="create-user"),
    path('test/', test.test, name="test"),
]
