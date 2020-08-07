from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Message
from django.db.models import Q
from django.contrib.auth.models import User
from datetime import datetime
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.core import serializers




# Create your views here.

def homepage(request):
    return render(request,'MessagingApp/index.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'MessagingApp/signup.html', {'form': form})

def about(request):
    return render(request,'MessagingApp/about.html')

def inbox(request, pk):
    pk = int(pk)
    chatnames = []
    if request.user.id == pk:
        messages = Message.objects.filter(Q(recipientId=pk) | Q(senderId=pk))
        for i in messages:
            if i.senderId not in chatnames:
                chatnames.append(i.senderId)
            if i.recipientId not in chatnames:
                chatnames.append(i.recipientId)
            chatnames.remove(request.user)
        return render(request, 'MessagingApp/inbox.html', {'chatnames':chatnames,'pk':str(pk)})
    else:
        return redirect('restricted')

def new(request, upk):
    upk = int(upk)
    if request.method == 'POST':
        try:
            sender = User.objects.get(username = request.POST.get('userName'))
            recipient = User.objects.get(id = upk)
            message = Message()
            message.senderId = sender
            message.recipientId = recipient
            message.dateTime = datetime.now()
            message.body = str(recipient.username + ' started a chat with ' + sender.username)
            message.save()
            return redirect('/' + str(upk) + '/inbox/' + sender.username + '/inboxDetails' ) 
        except:
            errors = "The username you are looking for does not exist."
            return render(request, 'MessagingApp/new.html',{'userId':upk, 'errors':errors})

    
    
    if request.user.id == upk:
       return render(request, 'MessagingApp/new.html',{'userId':upk})
    else:
        return redirect('restricted')

def logout_view(request):
    logout(request)
    return redirect('homepage')

def inboxDetails(request, upk, name):
    if request.method == 'POST':
        if request.POST.get('senderId') and request.POST.get('recipientId') and request.POST.get('message'):
            usermessage = "Your message has been sent."
            sender = User.objects.get(username = request.POST.get('recipientId'))
            recipient = User.objects.get(username = request.POST.get('senderId'))
            message = Message()
            message.senderId = sender
            message.recipientId = recipient
            message.dateTime = datetime.now()
            message.body = str(request.POST.get('message'))
            message.save()
        else:
            usermessage = "Unable to send your message."
    name = str(name)
    chatname = User.objects.get(username=name)
    upk = int(upk)
    currentuser = request.user
    if request.user.id == upk:
        messages = Message.objects.filter(Q(recipientId=currentuser, senderId=chatname) | Q(recipientId=chatname, senderId=currentuser)).order_by('dateTime') 
        readMessages = messages.select_for_update().filter(senderId=currentuser)
        return render(request, 'MessagingApp/inboxDetails.html', {'messages':messages, 'currentuser':currentuser, 'chatname': chatname})
    else:
        return redirect('restricted')

def getMessages(request, upk, name):
    name = str(name)
    chatname = User.objects.get(username=name)
    upk = int(upk)
    currentuser = request.user
    if request.user.id == upk:
        messages = list(Message.objects.filter(Q(recipientId=currentuser, senderId=chatname) | Q(recipientId=chatname, senderId=currentuser)).order_by('dateTime'))
        data = serializers.serialize('json', messages)
        return HttpResponse(data, content_type="application/json")
    else:
        return redirect('restricted')

def delete(request, upk, name):
    if request.method == 'POST':    
        name = str(name)
        chatname = User.objects.get(username=name)
        upk = int(upk)
        currentuser = request.user
        if request.user.id == upk:
            messages = Message.objects.filter(Q(recipientId=currentuser, senderId=chatname) | Q(recipientId=chatname, senderId=currentuser)).delete() 
            return redirect('/' + str(upk) + '/inbox')
        else:
            return redirect('restricted')
    if request.user.id == upk:
        chatname = User.objects.get(username=name)
        return render(request,'MessagingApp/delete.html',{'chatname':chatname})
    else:
        return redirect('restricted')


def restricted(request):
    return render(request,'MessagingApp/restricted.html')

