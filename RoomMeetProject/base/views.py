from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm



def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    counts = rooms.count()
    topics = Topic.objects.all()

    news = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')

    context = {'rooms': rooms, 'topics': topics, 'counts': counts, 'news': news}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)

    room_messages = room.message_set.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            body=request.POST.get('body'),
            room=room
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    participants = room.participants.all()

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def profile(request, pk):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.filter(Q(topic__name__icontains=q))
    news = user.message_set.filter(Q(room__topic__name__icontains=q))
    
    context = {'user': user, 'topics': topics, 'news': news, 'rooms': rooms}
    
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form,'topics': topics}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed to do this')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('room', pk=room.id)

    context = {'form': form, 'topics':topics, 'room': room}
    return render(request, 'base/create_room.html', context)


@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed to do this')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    room = Room.objects.get(id=message.room.id)

    if request.user != message.user:
        return HttpResponse('You are not allowed to do this')

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=room.id)

    context = {'obj': message}
    return render(request, 'base/delete.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not correct')

    context = {}

    return render(request, 'base/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {'form': form}

    return render(request, 'base/signup.html', context)


@login_required(login_url='login')
def edit_user(request, pk):
    form = UserForm(instance=request.user)
    
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES, instance=request.user)
        
        if userform.is_valid():
            userform.save()
            return redirect('profile', pk=request.user.id)
    
    context = {'form': form}
    return render(request, 'base/edit_user.html', context)


def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(Q(name__icontains=q))
    
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_page(request):
    messages = Message.objects.all()
    
    context = {'messages': messages}
    return render(request, 'base/activity.html', context)