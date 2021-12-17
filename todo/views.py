import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
import users.models
from .models import *


def index(request):
    # print("index::")
    # print(request.session['thisnickname'])
    # print(request.session['thisid'])
    if not request.session.get('has_login', None):
        message = "尚未登陆，请先登陆"
        return render(request, 'todo/index.html', locals())
    superuser = users.models.MyUser.objects.filter(id=request.session['u_id']).first()
    # print(superuser.id)
    # 当前用户还未注册todo app
    if todoUser.objects.filter(superuser=superuser).count() == 0:
        print(1085)
        not_for_this_app = 'true'
        return render(request, 'todo/index.html', locals())
    else:
        print(1086)
        request.session['thisnickname'] = todoUser.objects.filter(superaccount=superuser.account).first().mynickname
        request.session['thisid'] = todoUser.objects.filter(superaccount=superuser.account).first().id
        return init(request)
        # return render(request, 'todo/index.html', locals())


def init(request):
    u_id = request.session['thisid']
    user = todoUser.objects.get(id=u_id)
    lists = user.todolist_set.all()
    listmap = {}
    # listmap['lists'] = lists

    for i in lists:
        listmap[str(i.id)] = i.todoitem_set.all().order_by('-p_time')

    return render(request, 'todo/test.html', locals())


def register(request):
    u_id = request.session.get('u_id')
    print("TODO::\nregister:")
    print(request.session['u_id'])
    print(request.session['nickname'])
    superuser = users.models.MyUser.objects.filter(id=u_id).first()
    user = todoUser()
    user.superuser = superuser
    user.superaccount = superuser.account
    user.mynickname = superuser.nickname
    if request.method == 'POST':
        user.mynickname = request.POST.get('mynickname')
    request.session['thisnickname'] = user.mynickname
    request.session['thisid'] = user.id
    user.save()
    return redirect('/todo')


def loaditem_ajax(request, id):
    item = get_object_or_404(todoItem, id=id)
    res = {
        "itemname": item.item,
        "ctime": item.c_time.strftime('%Y/%m/%d %H:%M'),
        "ptime": item.p_time.strftime('%Y/%m/%d %H:%M'),
        "descrp": item.description,
        "statu": str(item.status),
    }
    print(res)
    return HttpResponse(json.dumps(res), content_type='application/json')


def deleteitem_ajax(request, id):
    item = get_object_or_404(todoItem, id=id)
    oc = True
    try:
        item.delete()
    except:
        oc = False
    return JsonResponse({"outcome": oc})


def finishitem_ajax(request, id):
    item = get_object_or_404(todoItem, id=id)
    oc = True
    try:
        item.f_time = datetime.datetime.now()
        item.status = 1
        item.save()
    except:
        oc = False
    return JsonResponse({"outcome": oc})


def giveupitem_ajax(request, id):
    item = get_object_or_404(todoItem, id=id)
    oc = True
    try:
        item.status = 2
        item.save()
    except:
        oc = False
    return JsonResponse({"outcome": oc})


def deletelist_ajax(request, id):
    item = get_object_or_404(todoList, id=id)
    oc = True
    try:
        item.delete()
    except:
        oc = False
    return JsonResponse({"outcome": oc})


def makenewlist(request):
    if request.method == "GET":
        return render(request, "todo/list.html", {})
    else:
        u_id = request.session.get("thisid")
        user = todoUser.objects.filter(id=u_id).first()
        newlist = todoList()
        ln = request.POST['name']
        same_name_list = user.todolist_set.filter(listname=ln)
        if same_name_list.count() == 0:
            newlist.user = user
            newlist.listname = ln
            newlist.description = request.POST['description']
            newlist.save()
            return JsonResponse({"res": "ss", "msg": "分组创建成功"})
        return JsonResponse({"res": "ff", "msg": "分组名已存在"})


def makenewitem(request):
    if request.method == "GET":
        u_id = request.session.get("thisid")
        user = todoUser.objects.filter(id=u_id).first()
        lists = user.todolist_set.all()
        data = {}
        for i in lists:
            data[str(i.id)] = i.listname
        return render(request, "todo/item.html", locals())
    else:
        itemname = request.POST["name"]
        thelist = todoList.objects.filter(id=request.POST['thelist']).first()
        same_name_item = thelist.todoitem_set.filter(item=itemname)
        newitem = todoItem()
        if same_name_item.count() == 0:
            newitem.item = itemname
            newitem.description = request.POST['description']
            newitem.p_time = request.POST['ptime']
            newitem.list = thelist
            newitem.save()
            return JsonResponse({"res": "ss", "msg": "事件创建成功"})
        return JsonResponse({"res": "ff", "msg": "分组名已存在"})
