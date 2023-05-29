from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(
        attrs={"id": "login", "placeholder": "Имя пользователя", 'name':"login"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"id": "password", "placeholder": "Пароль", 'name':"password"}))
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput(
        attrs={"id": "check_password", "placeholder": "Повторите пароль", 'name':"check_password"}))

    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}


class CreatePostForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":'Введите название'}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Введите описание"}))
    photo = forms.ImageField(required=False)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput(
        attrs={"id": "login", "placeholder": "Имя пользователя", 'name':'login'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={"id": "password", "placeholder": "Пароль", 'name':'password'}))

    class Meta:
        model = User
        fields = {'username', 'password'}


class CreateCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Введите комментарий"}))


