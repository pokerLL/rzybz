from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.log_in),
    # path('index/', views.index),
    path('login/', views.log_in),
    path('logout/', views.log_out),
    path('register/', views.register),
    path('confirm/', views.user_confirm),
]