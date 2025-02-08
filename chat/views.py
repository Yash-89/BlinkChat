from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

CustomUser = get_user_model()

def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'room': room,
        'username': username,
        'room_details': room_details,
    })

def login(request):
    username = request.POST['username']
    room = request.POST['room_name']
    flag = 1

    for char in username:
        if char != ' ':
            flag = 0
            break
    
    if flag == 1:
        messages.info(request, "Invalid Username")
        return redirect('/')

    if Room.objects.filter(name=room).exists() == False:
        new_room = Room.objects.create(name=room)
        new_room.save()

        return redirect('/' + room + '/?username=' + username)
    
    return redirect('/' + room + '/?username=' + username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_msg = Message.objects.create(msg=message, user=username, room=room_id)
    new_msg.save()

    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)

    return JsonResponse({'messages': list(messages.values())})

def register(request):
    return render(request, 'register.html')

def signup(request):
    if request.method == 'POST':
        usrnm = request.POST['username']
        dob = request.POST['dob']
        pswrd = request.POST['password']
        pswrd2 = request.POST['c_password']

        if pswrd == pswrd2:
            if CustomUser.objects.filter(username=usrnm).exists():
                messages.info(request, 'Username already used!')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(
                    username=usrnm,
                    dob=dob,
                    password=pswrd
                )
                user.save()
                return redirect('/')
        else:
            messages.info(request, 'The passwords are not matching')
            return redirect('register')
    else:
        return render(request, 'register.html')
    

def profile(request, usrnm):
    user = CustomUser.objects.get(username=usrnm)
    return render(request, 'profile.html', {'user': user})
