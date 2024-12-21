from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

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

def checkview(request):
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

    new_msg = Message.objects.create(value=message, user=username, room=room_id)
    new_msg.save()

    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)

    return JsonResponse({'messages': list(messages.values())})