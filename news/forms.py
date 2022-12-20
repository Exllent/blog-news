import re
from django.core.exceptions import ValidationError
from django import forms
from .models import News
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField


# class NewsForm(forms.Form):
#     title = forms.CharField(max_length=150, label='Название', widget=forms.TextInput
#     (attrs={'class': 'form-control'}))
#
#     content = forms.CharField(label='Текст', required=False, widget=forms.Textarea
#     (attrs={'class': 'form-control', 'rows': 5}))
#
#     is_published = forms.BooleanField(label='Опубликованно ?')
#
#     category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(),
#     widget=forms.Select(attrs={'class': 'form-control'}), empty_label='Выберите категорию')


class SignalForm(forms.Form):
    subject = forms.CharField(label='Тематика', widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label='Описание', widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', help_text='Password must be int',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', help_text='Repeat password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError("Название не должно начинаться с цыфры")
        return title
