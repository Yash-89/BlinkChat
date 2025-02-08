from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:room>/', views.room, name='room'),
    path('login', views.login, name='login'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('register', views.register, name='register'),
    path('signup', views.signup, name='signup')
]