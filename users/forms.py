from django import forms
from captcha.fields import CaptchaField


class loginForm(forms.Form):
    account = forms.CharField(label="账号", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Account", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')


class registerForm(forms.Form):
    gender = (
        ('male', 'man'),
        ('female', 'woman'),
        ('unknown', 'unknown'),
    )
    nickname = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    account = forms.CharField(label="账号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='性别', choices=gender)
    birthday = forms.DateField(label='生日', widget=forms.DateInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="城市", max_length=256,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'value': 'unknown'}))
    # description = forms.Textarea(label="个人描述", widget=forms.TextInput(attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='验证码')
