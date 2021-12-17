import hashlib

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta

# Create your views here.
from .forms import *
from .models import *
# from . import users_settings
from django.conf import settings


def index(request):
    if request.session.get('has_login', None):
        return render(request, 'users/index.html', locals())
    print('please log in')
    # message = '请先登陆'
    return redirect('/users/login/')


def log_in(request):
    # print(request.get_full_path())
    if request.session.get('has_login', None):
        print('has_login')
        return redirect('/')
    if request.method == 'POST':
        lgf = loginForm(request.POST)
        if lgf.is_valid():
            account = lgf.cleaned_data.get('account')
            password = lgf.cleaned_data.get('password')
            # user = get_object_or_404(MyUser, account=account)
            try:
                user = MyUser.objects.get(account=account)
            except:
                message = '账号不存在'
                return render(request, 'users/login.html', locals())

            if not user.has_confirmed:
                message = '账号未验证，请验证后再登陆'
                return render(request, 'users/login.html', locals())

            if user is not None:
                if password == user.password:
                    request.session['has_login'] = 'yes'
                    request.session['nickname'] = user.nickname
                    request.session['u_id'] = user.id
                    return redirect('/')
            message = '密码错误!'

            return render(request, 'users/login.html', locals())
        else:
            message = '请检查表单输入!'
            return render(request, 'users/login.html', locals())
    else:
        lgf = loginForm()
        return render(request, 'users/login.html', locals())


def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def log_out(request):
    request.session.flush()
    lgf = loginForm()
    message = "已成功退出登陆"
    # return render(request, '/', locals())
    return redirect('/')


def make_confirm_string(user):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hash_code(user.account, now)
    return code


def send_email(email, code):
    host_name = "121.4.176.100"
    from django.core.mail import EmailMultiAlternatives
    subject = '来自www.rzybz.fun的注册确认邮件'

    text_content = '''感谢注册www.rzybz.fun，\
                    如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员！'''

    html_content = '''
                    <p>感谢注册<a href="http://{}/users/confirm/?code={}" target=blank>www.rzybz.fun</a>，\
                    测试测试测试</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format(host_name, code, settings.EMAIL_CONFIRM_EXPIRE_TIME)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# 检查用户名和邮箱是否唯一
def register(request):
    if request.method == 'POST':
        rgf = registerForm(request.POST)
        message = "请检查表单内容！"
        if rgf.is_valid():
            account = rgf.cleaned_data.get('account')
            password1 = rgf.cleaned_data.get('password1')
            password2 = rgf.cleaned_data.get('password2')
            email = rgf.cleaned_data.get('email')
            print(account, password1, password2, email)
            if password1 != password2:
                message = "两次密码不一致，请重新输入！"
                return render(request, 'users/register.html', locals())

            # 未检查用户名和邮箱唯一性
            same_account_user = MyUser.objects.filter(account=account)

            if same_account_user.count() != 0:
                message = "账号已被注册，请更换账号！"
                return render(request, 'users/register.html', locals())

            same_email_user = MyUser.objects.filter(email=email)
            if same_email_user.count() != 0:
                message = "邮箱已被绑定，请更换邮箱！"
                return render(request, 'users/register.html', locals())

            user = MyUser()
            user.nickname = rgf.cleaned_data.get('nickname')
            user.account = account
            user.password = password1
            user.email = rgf.cleaned_data.get('email')
            user.birthday = rgf.cleaned_data.get('birthday')
            user.gender = rgf.cleaned_data.get('gender')
            user.city = rgf.cleaned_data.get('city')
            user.has_confirmed = False

            # print(user)

            code = make_confirm_string(user)
            send_email(email, code)
            user.save()
            confirm = ConfirmStatus.objects.create(code=code, user=user)
            confirm.save()
            lgf = loginForm()
            message = "已成功注册，请前往邮箱验证！"
            return render(request, 'users/login.html', locals())
        else:
            return render(request, 'users/register.html', locals())

    else:
        rgf = registerForm()
        return render(request, 'users/register.html', locals())
    # pass


def user_confirm(request):
    code = request.GET.get('code', None)
    message = ""
    print(code)

    try:
        confirm = ConfirmStatus.objects.get(code=code)
    except:
        message = '无效的确认请求'
        return render(request, 'users/confirm.html', locals())

    c_time = confirm.c_time
    now = datetime.now()
    if now > c_time + timedelta(settings.EMAIL_CONFIRM_EXPIRE_TIME):
        confirm.user.delete()
        message = '您的邮件已经过期！请重新注册!'
        return render(request, 'users/confirm.html', locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录！'
        return render(request, 'users/confirm.html', locals())
