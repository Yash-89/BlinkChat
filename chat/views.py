from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

CustomUser = get_user_model()

def home(request):
    return render(request, 'home.html')

@login_required
def room(request, room):
    username = request.GET.get('username')
    if username != request.user.username:
        messages.info(request, 'Something went wrong!')
        return redirect('/')
    
    if not Room.objects.filter(name=room).exists():
        messages.info(request, "The Room '" + room + "' does not exist!")
        return redirect('/')

    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'room': room,
        'username': username,
        'room_details': room_details,
    })

def login(request):
    if request.user.is_authenticated:
        room = request.POST.get('room_name')

        if not Room.objects.filter(name=room).exists():
            new_room = Room.objects.create(name=room)
            new_room.save()

        return redirect('/' + room + '/?username=' + request.user.username)
    elif request.method == 'POST':
        usrnm = request.POST['username']
        pswrd = request.POST['password']

        user = auth.authenticate(username=usrnm, password=pswrd)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials!')
            return redirect('/')
    else:
        return render(request, 'home.html')

    # username = request.POST['username']
    # room = request.POST['room_name']

    # if Room.objects.filter(name=room).exists() == False:
    #     new_room = Room.objects.create(name=room)
    #     new_room.save()

    #     return redirect('/' + room + '/?username=' + username)
    
    # return redirect('/' + room + '/?username=' + username)

def logout(request):
    auth.logout(request)
    return redirect('/')

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_msg = Message.objects.create(
        msg=message,
        user=username,
        room=room_id,
    )
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

        flag = 1

        for char in usrnm:
            if char != ' ':
                flag = 0
                break
        
        if flag == 1:
            messages.info(request, "Invalid Username")
            return redirect('register')

        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        currDate = datetime.now().date()

        if dob_date > currDate:
            messages.info(request, 'Date of birth cannot exceed the current day.')
            return redirect('register')

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
    
@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})
