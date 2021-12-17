from django.db import models
from datetime import datetime


# Create your models here.

class MyUser(models.Model):
    gender = (
        ('male', 'man'),
        ('female', 'woman'),
        ('unknown', 'unknown'),
    )
    nickname = models.CharField(max_length=256, unique=False, default='default')
    account = models.CharField(max_length=256, unique=True)
    password = models.CharField(max_length=256)
    is_vaild = models.BooleanField(default=True, verbose_name="账号有效")
    has_confirmed = models.BooleanField(default=False, verbose_name="已进行邮箱验证")
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=32, choices=gender, default='unknown')
    birthday = models.DateField(default=datetime.strptime('1970-1-1', '%Y-%m-%d'), blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
    remark = models.CharField(max_length=256, blank=True, default='')
    description = models.CharField(max_length=256, blank=True, default='说点啥吧。')

    def __str__(self):
        return self.account

    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ConfirmStatus(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-c_time']
        verbose_name = '验证码'
        verbose_name_plural = '验证码'
