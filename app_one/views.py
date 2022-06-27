from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
import random
from datetime import datetime
from django.urls import reverse
from app_one.models import User,Listwish
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):

    return render(request, "main.html")



def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST["password"]
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode(), salt)

            password_confirem = request.POST["confirem-password"]
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password_confirem.encode(), salt)

            user = User()
            user.name = request.POST["name"]
            user.username = request.POST["username"]
            user.data_hired= request.POST["data_hired"]
            user.password = hash.decode()
            user.password_confirem = hash.decode()
            user.save()
            messages.success(request, "Register User successfully")
            request.session["userId"] = user.id
            return redirect('/')
    return render(request, "main.html") 

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
             user = User.objects.get(username=username)
             if bcrypt.checkpw(password.encode(), user.password.encode()):
                 request.session["userId"] = user.id
                 messages.success(request, "Login User successfully")
                 return redirect(reverse('allWish'))

             else:  
                 messages.error(request, "password dosn't match")
                 return redirect('/') 

        except User.DoesNotExist:
                 messages.error(request, "userName does not exist")
                 return redirect('/')
    return render(request, "main.html")


def addWish(request):
  user = User.objects.get(id=request.session["userId"])  
  if request.method == "POST":
    errors = Listwish.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wish_item/create')

    else:
        item = request.POST["item"]
        userName = request.POST.get("user.name")
        user_name= User.objects.get(name = userName)
        item = Listwish.objects.create(item=item, user_name=user_name)
        return redirect("/dashboard")
  context ={
        "user" : user
       }
   
  return render(request, "add-wish.html",  context)


def logout(request):
    request.session.clear()
    return redirect('/')


def allWish(request):
    user = User.objects.get(id=request.session["userId"])
    context = {
      "user": user,
      "users": User.objects.all(),
      "items": Listwish.objects.all(),
    }
    return render(request, "wish-list.html", context)


def showItem(request, itemId):
    item = Listwish.objects.get(id=itemId)
    context = {
        "item": item,
        "users": User.objects.all(),
        "items": Listwish.objects.all(),
    }
    return render(request, "show-item.html", context)    


def delteItem(request, ItemId):
    Listwish.objects.filter(id=ItemId).delete() 
    return redirect(reverse('allWish'))


def addListToUser(request, ItemId):
    user = User.objects.get(id=request.session["userId"])
    item = Listwish.objects.get(id=ItemId)
    user.itemwish.add(item)   #add book to author 
    user.save()
        
    items = Listwish.objects.all()
    context = {
        "user": user,
        "items": items
    }
    return render(request, "wish-list.html", context)    


def removeItem(request, ItemId):
    user = User.objects.get(id=request.session["userId"])
    item = Listwish.objects.get(id=ItemId)
    user.itemwish.remove(item)
    user.save()
    return redirect(reverse('allWish'))

    ##remove()