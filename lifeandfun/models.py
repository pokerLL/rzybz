from django.db import models

# Create your models here.
import users.models


class lifeUser(models.Model):
    '''
    已有字段：
    name，word，is_vaild，has_confirmed，email，
    gender，birthday，city，c_time,u_time,remark
    '''

    mynickname = models.CharField(max_length=256, default='default')
    superaccount = models.CharField(max_length=256, default='default', null=True)
    superuser = models.ForeignKey('users.MyUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.mynickname

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class lifeTag(models.Model):
    tagname = models.CharField(max_length=50)

    def __str__(self):
        return self.tagname

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class lifeArticle(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('lifeUser', on_delete=models.CASCADE)
    username = models.CharField(max_length=256, default='default')
    tags = models.ManyToManyField('lifeTag')
    content = models.TextField()
    description = models.TextField(max_length=256, default='')
    poll_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    view_num = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-c_time']
        verbose_name = '文章'
        verbose_name_plural = '文章'


class lifeComment(models.Model):
    article = models.ForeignKey('lifeArticle', on_delete=models.CASCADE)
    user = models.ForeignKey('lifeUser', on_delete=models.CASCADE)
    username = models.CharField(max_length=256, default='')
    comment = models.ForeignKey('lifeUser', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    for_comment = models.BooleanField(default=False)
    content = models.TextField(max_length=1024)
    poll_num = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.article.title + ': ' + self.content

    class Meta:
        ordering = ['-c_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'


class lifePoll(models.Model):
    article = models.ForeignKey('lifeArticle', on_delete=models.CASCADE)
    user = models.ForeignKey('lifeUser', on_delete=models.CASCADE)
    username = models.CharField(max_length=256, default='')
    comment = models.ForeignKey('lifeComment', on_delete=models.CASCADE, null=True)
    for_comment = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)
    u_time = models.DateTimeField(auto_now=True)
