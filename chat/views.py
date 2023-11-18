import string
import secrets
from django.shortcuts import render, redirect
from .models import Room, Message
from .forms import CreateRoomForm, JoinRoomForm
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore


def home(request):
    return render(request, 'chat/home.html')

def generate_room_id():
    characters = string.ascii_letters + string.digits
    room_id = '-'.join([''.join(secrets.choice(characters) for _ in range(5)) for _ in range(4)])
    return room_id

def create_room(request):
    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            max_users = form.cleaned_data['max_users']
            password = form.cleaned_data['password']
            expiration_time = timezone.now() + timezone.timedelta(hours=2)

            room_id = generate_room_id()

            room = Room.objects.create(room_id=room_id, max_users=max_users, password=password, expiration_time=expiration_time)
            return redirect('chat:room', room_id=room.room_id)
    else:
        form = CreateRoomForm()
    return render(request, 'chat/create_room.html', {'form': form})



def join_room(request):
    if request.method == 'POST':
        form = JoinRoomForm(request.POST)
        if form.is_valid():
            room_id = form.cleaned_data['room_id']
            password = form.cleaned_data['password']

            try:
                room = Room.objects.get(room_id=room_id)
                if password == room.password:
                    request.session['room_password'] = password  # Store room password in the session
                    return redirect('chat:room', room_id=room.room_id)
                else:
                    form.add_error('password', 'Incorrect password')
            except Room.DoesNotExist:
                form.add_error('room_id', 'Room does not exist')

    else:
        form = JoinRoomForm()

    return render(request, 'chat/join_room.html', {'form': form})



def room(request, room_id):
    try:
        room = Room.objects.get(room_id=room_id)
    except Room.DoesNotExist:
        return redirect('chat:home')

    # Check if the user has the correct room password in the session or in the form
    if request.method == 'POST':
        password = request.POST.get('password', '')
        if password == room.password:
            request.session['room_password'] = password  # Store room password in the session
        else:
            return render(request, 'chat/room_password.html', {'room_id': room_id})

    # Check if the user has the correct room password in the session
    if request.session.get('room_password') != room.password:
        return render(request, 'chat/room_password.html', {'room_id': room_id})

    messages = Message.objects.filter(room=room)

    if request.method == 'POST':
        content = request.POST.get('content', '')
        sender = request.session.get('user_name', '')
        if not sender:  # If user_name is not in the session, ask for it.
            sender = request.POST.get('sender', '')
            request.session['user_name'] = sender  # Store user_name in the session

        Message.objects.create(room=room, content=content, sender=sender)

    return render(request, 'chat/room.html', {'room': room, 'messages': messages})

