from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'), 
    path('register', views.register, name='register'),
    path('login', views.login), 
    path('wish_item/create', views.addWish, name='addWish'), 
    path('logut', views.logout, name='logout'),
    path('dashboard', views.allWish, name='allWish'), 
    path('item/<int:itemId>', views.showItem, name="showItem"),
    path('delete/<int:ItemId>',views.delteItem, name='delteItem'), ## delete
    path('remove/<int:ItemId>',views.removeItem, name='removeItem'), ## remove
    path('addlisttouser/<int:ItemId>',views.addListToUser, name='addListToUser'),
]    