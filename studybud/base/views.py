

from django. shortcuts import render,redirect
from django. db.models import Q
from .models import Room, Message, Topic, User
from .forms import RoomForm, UserForm,MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

def home(request):
    #q = request.GET.get('q') if request.GET.get('q') != None else ('')
    if request.GET.get('q') != None: #IF SOMETHING ENTERS IN THE URL OF HOME PAGE AS q
        q = request.GET.get('q')     # recieve its value into variable q else 'q' have value ''(empty string)
    else:
        q = ''
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) #recive the filtered Message class objects
                                                                              # if 'q' contain any letters of the topic name those messages 
    ROOM = Room.objects.filter(                                                #those messages are retrived
        Q(topic__name__icontains =q)|# retrive the rooms based on the values of q, if q contain any letters regarding topic name or 
        Q(name__icontains =q)|          # room name or description
        Q(description__icontains =q))
    room_count = ROOM.count()           # find the number of rooms recived on ROOM variable
    topic = Topic.objects.all()[0:5]    # this will recive the first 5 topic objects
    context = {'rooms':ROOM, 'room_count':room_count, 'topic':topic , 'room_messages':room_messages,}
    return render(request,"base/home.html" , context)

def room(request, pk): # this is a view function for displaying the specific room when the user clickson them
    ROOM = Room.objects.get(id=pk) # reterving the one room object based on the id of the clicked room
    room_messages = ROOM.message_set.all().order_by('-created')# retreving the all the messages of the specific room object 
    participants = ROOM.participants.all() # retreving all the participats of the specific room
    if request.method == 'POST':# in the room.html we have a functionality of submiting messages with post method
        body = request.POST.get('message') # receving the input field with the name message(this is the body of the message)
        user =request.user  #setting the user
        room = ROOM         # setting the user
        Message.objects.create(user=user, body=body, room=room) # creating the user using create mehtod 
        ROOM.participants.add(request.user) # adding a participants to the specific room 
        return redirect('room', pk=ROOM.id) # after submitting the message returning to the same page
    context = {'room': ROOM , 'room_messages':room_messages, 'participants':participants}
    return render(request, "base/room.html", context) # rendering the room.html page and adding context to the specific page

def userProfile(request,pk): # this is the function that displays the user profile page 
    user = User.objects.get(id=pk) # selecting the specific user object
    rooms = user.room_set.all() # selecting the rooms that are created by the specified user 
    room_message = user.message_set.all() # selecting all the messages that are created by the specific user 
    topics = Topic.objects.all() # selecting all the avilabel topic (ont only the ones that are created by the specific user)
    room = Room.objects.all() # selecting all the rooms (not ony the ones that are created by the specific user ) this is only to count the room number
    room_count = room.count() # counding all the rooms thare avilible on the entire website
    context = {'user':user,'rooms':rooms,'topic':topics,'room_messages':room_message,'room_count':room_count,}
    return render(request,'base/user_profile.html',context)

def deleteMessage(request, pk): # this is a function for deleting the messages that are created by a specific user (the owner of the message)
    message = Message.objects.get(id=pk) # getting the specific message 
    if request.user != message.user: # checking wether the requested user is the owner of the message or not (if not)
        return HttpResponse('you are not allowed here') # sending them a message
    if request.method == 'POST': # if the method is a post (a post method in this function is submitted by only usser)
        message.delete()
        return redirect('home') # delete the message and go back to the home page 
    return render(request,'base/delete.html', {"obj":message})

@login_required(login_url = 'login') # checking wether the user is logged in or not if not sending him to the login page
def createRoom(request): # this is the function for creating a home page 
    form = RoomForm() # creating a form object by using the imported class RoomForm
    topics = Topic.objects.all() # retreving all the topic to add the avilable topics to the dropdown list of the specified html page
    if request.method == 'POST': # if the request from the webpage is a POST method 
        topic_name = request.POST.get('topic') # receving the topic from the input field named topic
        topic, created = Topic.objects.get_or_create(name= topic_name) # checking is there any topic in the Topic objects with the name of 
                                                                    # the recieved topic if yes retreving that topic object if no create a
                                                                    # Topic object with that name and return it 
        Room.objects.create(
            host = request.user,
            topic = topic,                                  # creating the room with the specified  vlaues
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
   
        return redirect('home')
    context = {'form':form, 'topic':topics}
    return render(request,'base/form-room.html',context)


@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return  HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name= topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context ={'form':form, "room":room, "topics":topics }
    return render(request,'base/form-room.html',context)

@login_required(login_url = 'login')
def deleteRoom(request, pk): 
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return  HttpResponse('You are not allowed here!!!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
        
    context = {'obj':room}

    return render(request,'base/delete.html',context)

def loginPage(request):
    page = 'login'
    if request.user. is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request, "user does not exist ")
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'username and password does not match')
    context = {'page':page}        
    return render(request, 'base/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit= False)
            user.username = user.username.lower()
            user.save()

            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')    
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request,'base/settings.html',{"form":form,})


def topic(request):
    if request.GET.get('q')!= None:
        q = request.GET.get('q') 
    else:
        q =''
    topics = Topic.objects.filter(name__icontains=q)

    context ={'topics':topics,}
    return render(request,'base/topics.html', context)

def activity(request):
    room_messages = Message.objects.all()

    context= {'room_messages':room_messages,}

    return render(request,'base/activity.html',context)