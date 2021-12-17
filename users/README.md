## 概述
本应用简称为users，users实现了用户的注册与登陆，注册和登陆都使用了图形验证码机制，其中注册时使用邮箱链接点击验证的形式。

user定义如下：

```python
class MyUser(models.Model):
    gender = (
        ('male', 'man'),
        ('female', 'woman'),
        ('unknown', 'unknown'),
    )
    name = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    is_vaild = models.BooleanField(default=True)
    has_confirmed = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=32, choices=gender, default='unknown')
    birthday = models.DateField(default=datetime.strptime('1970-1-1', '%Y-%m-%d'), blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=256, blank=True, default='')
```


## 配置注意点

1. 因在应用中使用了django-simple-captcha图形验证码库，因此需要提前安装这一库，并注册到根目录的setting下，可以同时对captcha做一些初始化，并设置根目录路由。
```python
# pip
pip install django-simple-captcha

# settings.py
INSTALLED_APPS = [
    'captcha',
    ...
]

    # CAPTCHA 
CAPTCHA_IMAGE_SIZE = (80,45)
CAPTCHA_LENGTH = 4
CAPTCHA_TIME_OUT = 1 #minute

CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_null',
    'captcha.helpers.noise_arcs',
    'captcha.helpers.noise_dots',
)

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'

# urls.py
path('captcha/', include('captcha.urls')),

# 点击验证码自动刷新的js代码
<script src="https://cdn.bootcss.com/jquery/1.12.3/jquery.min.js"></script>
    <script>
         //点击刷新验证码
        $(function () {
            $('.captcha').css({
                'cursor': 'pointer'
            });
            // ajax刷新
            $('.captcha').click(function () {
                console.log('click');
                $.get("{% url 'captcha-refresh' %}",
                    function (result) {
                        $('.captcha').attr('src', result['image_url']);
                        $('#id_captcha_0').val(result['key'])
                    });
            });
        })
    </script>

```

2. 因为在应用内部定义了邮件发送函数，因此需要在settings.py中定义一些参数，如下：
```python
# 邮件验证模块参数
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sina.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'rzybz1024@sina.com'
EMAIL_HOST_PASSWORD = '8a8b0436a8eafb3b'

EMAIL_CONFIRM_EXPIRE_TIME = 1 # day

```

## 总结

1. 万万不能直接cv代码，因为目录和资源的不同位置可能导致很难进行debug<血的教训>。