# Generated by Django 3.2.8 on 2021-12-17 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='chatUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mynickname', models.CharField(default='default', max_length=256)),
                ('superaccount', models.CharField(default='default', max_length=256)),
                ('superuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.myuser')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
            },
        ),
        migrations.CreateModel(
            name='chatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=1024)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
                ('forUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webchat.chatuser')),
                ('sendUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='webchat.chatuser')),
            ],
            options={
                'verbose_name': '信息',
                'verbose_name_plural': '信息',
            },
        ),
    ]
