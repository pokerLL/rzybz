from django.shortcuts import render, redirect
import users.models
from .models import *


def index(request):
    # print("index::")
    # print(request.session['thisnickname'])
    # print(request.session['thisid'])
    if not request.session.get('has_login', None):
        message = "尚未登陆，请先登陆"
        return render(request, 'webchat/index.html', locals())
    superuser = users.models.MyUser.objects.filter(id=request.session['u_id']).first()
    # print(superuser.id)
    # 当前用户还未注册webchat app
    if chatUser.objects.filter(superuser=superuser).count() == 0:
        print(1085)
        not_for_this_app = 'true'
        return render(request, 'webchat/index.html', locals())
    else:
        print(1086)
        request.session['thisnickname'] = chatUser.objects.filter(superaccount=superuser.account).first().mynickname
        request.session['thisid'] = chatUser.objects.filter(superaccount=superuser.account).first().id
        return render(request, 'webchat/index.html', locals())


def poll(request):
    pass


def push(request):
    pass


def register(request):
    u_id = request.session.get('u_id')
    # print(request.session['u_id'])
    # print(request.session['nickname'])
    superuser = users.models.MyUser.objects.filter(id=u_id).first()
    user = chatUser()
    user.superuser = superuser
    user.superaccount = superuser.account
    user.mynickname = superuser.nickname
    if request.method == 'POST':
        user.mynickname = request.POST.get('mynickname')
    request.session['thisnickname'] = user.mynickname
    request.session['thisid'] = user.id
    user.save()
    return redirect('/chat')
