from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('detail/<int:a_id>/', views.detail),
    path('poll/<int:a_id>/', views.poll),
    path('comment/', views.comment),
    path('tag/<int:tag_id>/', views.withtag),
    path('push/', views.pusharticle),
    path('register/', views.register),
]
