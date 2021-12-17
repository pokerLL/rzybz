from django.db import models
import datetime


# Create your models here.

class todoUser(models.Model):
    superuser = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)
    superaccount = models.CharField(max_length=256, default='default')
    mynickname = models.CharField(max_length=256, default='default')
    c_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.mynickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class todoList(models.Model):
    user = models.ForeignKey(todoUser, on_delete=models.CASCADE)
    listname = models.CharField(max_length=256, unique=True, default='default')
    c_time = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=256, default='')

    def __str__(self):
        return self.listname

    class Meta:
        verbose_name = '分组'
        verbose_name_plural = '分组'


class todoItem(models.Model):
    list = models.ForeignKey(todoList, on_delete=models.CASCADE)
    item = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)
    p_time = models.DateTimeField(default=datetime.datetime.now() + datetime.timedelta(days=1))
    f_time = models.DateTimeField(default=datetime.datetime.strptime('2000/01/01 00:00', '%Y/%m/%d %H:%M'))
    status = models.IntegerField(default=0)
    '''
    0 创建
    1 完成
    2 放弃
    '''
    description = models.CharField(max_length=256, default='')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '事件'
        verbose_name_plural = '事件'
