from django.db import models


# Create your models here.


class chatUser(models.Model):
    mynickname = models.CharField(max_length=256, default='default')
    superaccount = models.CharField(max_length=256, default='default')
    superuser = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.mynickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class chatMessage(models.Model):
    sendUser = models.ForeignKey(chatUser, related_name='+', on_delete=models.CASCADE)
    forUser = models.ForeignKey(chatUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.c_time.__str__() + ":" + self.content

    class Meta:
        verbose_name = '信息'
        verbose_name_plural = '信息'
