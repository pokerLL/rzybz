import markdown2
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
import users.models
from .models import *


def index(request):
    # print("index::")
    # print(request.session['thisnickname'])
    # print(request.session['thisid'])
    if not request.session.get('has_login', None):
        message = "尚未登陆，请先登陆"
        return render(request, 'lifeandfun/index.html', locals())
    superuser = users.models.MyUser.objects.filter(id=request.session['u_id']).first()
    # print(superuser.id)
    # 当前用户还未注册lifeandfun app
    if lifeUser.objects.filter(superuser=superuser).count() == 0:
        print(1085)
        not_for_this_app = 'true'
        return render(request, 'lifeandfun/index.html', locals())
    else:
        print(1086)
        request.session['thisnickname'] = lifeUser.objects.filter(superaccount=superuser.account).first().mynickname
        request.session['thisid'] = lifeUser.objects.filter(superaccount=superuser.account).first().id
        alltags = lifeTag.objects.all()
        # request.session['alltags'] = alltags
        articles = lifeArticle.objects.all().order_by('-poll_num')[:9]
        return render(request, 'lifeandfun/index.html', locals())


def detail(request, a_id):
    article = lifeArticle.objects.get(id=a_id)
    article.view_num += 1
    article.save()
    comments = lifeComment.objects.filter(article=article)
    author = article.author
    superuser = author.superuser
    content = markdown2.markdown(article.content)
    tags = article.tags.all()
    alltags = lifeTag.objects.all()
    return render(request, 'lifeandfun/detail.html', locals())


def poll(request, a_id):
    u_name = request.session.get('thisnickname', None)
    u_id = request.session['thisid']
    article = lifeArticle.objects.get(id=a_id)
    if u_name:
        if lifePoll.objects.filter(article=article, username=u_name).count() == 0:
            # print(u_name)
            poll = lifePoll.objects.create(username=u_name, user=lifeUser.objects.get(id=u_id),
                                           article=article)
            article.poll_num += 1
            article.save()
            poll.save()
    url = "/life/detail/" + str(a_id) + "/"
    return JsonResponse({})


def comment(request):
    a_id = request.POST.get('article_id', None)
    content = request.POST.get('content', None)
    article = lifeArticle.objects.get(id=a_id)
    username = request.session['thisnickname']
    user = lifeUser.objects.filter(mynickname=username).first()
    new_comment = lifeComment.objects.create(content=content, article=article,
                                             user=user, username=username)
    message = "成功发布！"
    # print(request.session['nickname'])

    new_comment.save()
    article.comment_num += 1
    article.save()

    url = "/life/detail/" + a_id + "/"
    return redirect(url, locals())


def withtag(request, tag_id):
    tag = lifeTag.objects.get(id=tag_id)
    articles = tag.lifearticle_set.all()
    return render(request, 'lifeandfun/listfortag.html', locals())


def pusharticle(request):
    if request.method == 'GET':
        return render(request, 'lifeandfun/editor.html', {})

    # is POST
    content = request.POST['content']
    title = request.POST['title']
    u_id = request.session['thisid']
    # print("PUSH ARTICLE")
    # print(u_id)
    # print(request.session['thisnickname'])

    # tags = request.POST.get('tags', None)
    # author = lifeUser.objects.get(mynickname=request.session['thisnickname'])
    author = lifeUser.objects.get(id=u_id)
    description = request.POST['description']
    if len(description) < 5:
        description = content[0:50]

    # print("content:")
    # print(content)
    # print("description:")
    # print(description)
    article = lifeArticle()
    article.author = author
    article.username = author.mynickname
    article.content = content
    article.title = title
    article.description = description
    article.save()
    return redirect('/life')


def register(request):
    u_id = request.session.get('u_id')
    # print(request.session['u_id'])
    # print(request.session['nickname'])
    superuser = users.models.MyUser.objects.filter(id=u_id).first()
    user = lifeUser()
    user.superuser = superuser
    user.superaccount = superuser.account
    user.mynickname = superuser.nickname
    if request.method == 'POST':
        user.mynickname = request.POST.get('mynickname')
    # print(user.mynickname)
    request.session['thisnickname'] = user.mynickname
    request.session['thisid'] = user.id
    user.save()
    return redirect('/life')
