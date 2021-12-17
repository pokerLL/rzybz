"""rzybz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register/', views.register),
    path('load/<int:id>/', views.loaditem_ajax),
    path('delete/<int:id>/', views.deleteitem_ajax),
    path('finish/<int:id>/', views.finishitem_ajax),
    path('giveup/<int:id>/', views.giveupitem_ajax),
    path('dellist/<int:id>/', views.deletelist_ajax),
    path('newlist/', views.makenewlist),
    path('newitem/', views.makenewitem),
]
