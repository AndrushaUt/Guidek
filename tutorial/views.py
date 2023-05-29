from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import  User
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.http import HttpRequest
from datetime import datetime
from copy import deepcopy

def index(request):
    return render(request, 'tutorial/index.html')


def auth(request: HttpRequest, status:int):
    if request.method == 'GET':
        return render(request, 'tutorial/login_form.html',
                      {'form': UserLoginForm})
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'tutorial/login_form.html',
                          {'form': UserLoginForm(),
                           'error': 'Пользователя с такими имя пользователя и паролем не существует'})
        else:
            login(request, user)
            if status == 1:
                return redirect('all_posts',1)
            return redirect('login_home')


def home(request: HttpRequest):
    posts = Guide.objects.values()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'tutorial/index.html',
                          {'form': form, 'posts': list(posts)[::-1][0:6]})
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'],
                                                password=request.POST[
                                                    'password1'])
            user.save()
            login(request, user)
            return redirect('login_home')
        else:
            return render(request, 'tutorial/index.html',
                          {'form': UserRegisterForm,
                           'error': 'Passwords do not match',
                           'posts': list(posts)[::-1][0:6]})
    else:
        form = UserRegisterForm()
    return render(request, 'tutorial/index.html', {'form': form, 'posts': list(posts)[::-1][0:min(len(list(posts)),9)]})

@login_required
def create(request: HttpRequest):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            try:
                t1 = Guide(**form.cleaned_data)
                t1.username = request.user.username
                t1.date = datetime.today()
                t1.description = " ".join(list(str(t1.content).split())[0:15])
                print(1)
                t1.save()
                return redirect('login_home')
            except:
                form.add_error(None, 'Ошибка')
    else:
        form = CreatePostForm()
    return render(request, 'tutorial/creation.html', {'form': form})


@login_required
def login_home(request: HttpRequest):
    posts = Guide.objects.values()
    return render(request, 'tutorial/login_home.html', {'user_name': request.user.username, 'posts': list(posts)[::-1][0:min(len(list(posts)),9)]})


def view_post(request: HttpRequest, post_num: int):
    post = Guide.objects.get(pk=post_num)
    liked = False
    if Like.objects.filter(to_post=post_num, username=request.user.username):
        liked = True
    if request.method == 'POST':
        form = CreateCommentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                t1 = Comment(**form.cleaned_data)
                t1.author = request.user.username
                t1.date = datetime.today()
                t1.to_post = post_num
                t1.save()
                return redirect('view_post',post_num)
            except:
                form.add_error(None, 'Ошибка')
    comments = Comment.objects.filter(to_post=post_num)
    return render(request, 'tutorial/post.html', {'post':post, 'form':CreateCommentForm(), 'comments':list(comments)[::-1],'liked':liked})


@login_required
def logoutaccount(request:HttpRequest, status:int):
    logout(request)
    if status == 0:
        return redirect('home')
    return redirect(request.META.get('HTTP_REFERER'))

def all_posts(request:WSGIRequest,page:int):
    searchPost = request.GET.get("searchPost")
    liked = list(map(lambda a:a.to_post,Like.objects.filter(username=request.user.username)))
    if searchPost:
        posts = Guide.objects.filter(title__icontains=searchPost)
        return render(request, 'tutorial/all_posts.html',
                      {'user_name': request.user.username,
                       'posts': list(posts)[::-1],
                       'page_num': page,
                       'prev_num': page - 1,
                       'next_num': page + 1,
                       'amount_of_all_post': len(Guide.objects.values()),
                       'max_amount_of_posts_in_current_page': page * 12,
                       'searchPost':searchPost,
                       'like_list':liked})
    else:
        posts = Guide.objects.values()
        return render(request, 'tutorial/all_posts.html',
                      {'user_name': request.user.username,
                       'posts': list(posts)[::-1][(page - 1)*12:min(len(list(posts)), page*12)],
                       'page_num': page,
                       'prev_num': page - 1,
                       'next_num': page + 1,
                       'amount_of_all_post':len(Guide.objects.values()),
                       'max_amount_of_posts_in_current_page':page * 12,
                       'searchPost':searchPost,
                       'like_list':liked})

def user_page(request,username,page:int):
    searchPost = request.GET.get("searchPost")
    posts_all = Guide.objects.filter(username = username)
    liked = list(map(lambda a: a.to_post,
                     Like.objects.filter(username=request.user.username)))
    date = None
    if posts_all:
        date = posts_all[len(posts_all) - 1].date
    if searchPost:
        posts = Guide.objects.filter(username=username,title__icontains=searchPost)
        return render(request, 'tutorial/profile.html',
                      {'user_name': username,
                       'posts': list(posts)[::-1],
                       'page_num': page,
                       'prev_num': page - 1,
                       'next_num': page + 1,
                       'amount_of_posts': len(Guide.objects.filter(username=username)),
                       'max_amount_of_posts_in_current_page': page * 12,
                       'searchPost': searchPost,
                       'date':User.objects.get(username=username).date_joined.date(),
                       'username_visitor':request.user.username,
                       'last_date':date,
                       'staff':User.objects.get(username=username).is_staff,
                       'like_list':liked})
    else:
        posts = Guide.objects.filter(username=username)
        return render(request, 'tutorial/profile.html',
                      {'user_name': username,
                       'posts': list(posts)[::-1][
                                (page - 1) * 12:min(len(list(posts)),
                                                    page * 12)],
                       'page_num': page,
                       'prev_num': page - 1,
                       'next_num': page + 1,
                       'amount_of_posts': len(posts),
                       'max_amount_of_posts_in_current_page': page * 12,
                       'searchPost': searchPost,
                       'date':User.objects.get(username=username).date_joined.date(),
                       'username_visitor':request.user.username,
                       'last_date':date,
                       'staff':User.objects.get(username=username).is_staff,
                       'like_list':liked})
@login_required
def edit(request, post_num:int):
    try:
        res = Guide.objects.get(username=request.user.username, pk=post_num)
    except Guide.DoesNotExist:
        return redirect('login_home')
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            try:
                t1 = Guide(**form.cleaned_data)
                t1.username = request.user.username
                t1.date = datetime.today()
                t1.description = " ".join(list(str(t1.content).split())[0:15])
                if not t1.photo:
                    t1.photo = res.photo
                t1.likes_amount = res.likes_amount
                t1.save()
                for comment in Comment.objects.filter(to_post=post_num):
                    comment1 = deepcopy(comment)
                    comment1.to_post = t1.pk
                    comment.delete()
                    comment1.save()
                for like in Like.objects.filter(to_post=post_num):
                    like1 = deepcopy(like)
                    like1.to_post = t1.pk
                    like.delete()
                    like1.save()
                res.delete()
                return redirect('user_page',request.user.username,1)
            except:
                form.add_error(None, 'Ошибка')
    else:
        form = CreatePostForm(model_to_dict(res))
    print(res.pk)
    return render(request, 'tutorial/edit.html', {'form': form,'res':res})

@login_required
def delete_post(request,post_num:int):
    try:
        res = Guide.objects.get(username=request.user.username, pk=post_num)
        for comment in Comment.objects.filter(to_post=post_num):
            comment.delete()
        res.delete()
        return redirect('user_page',request.user.username,1)
    except Guide.DoesNotExist:
        return redirect('login_home')


@login_required
def delete_comment(request,comment_num:int):
    try:
        res = Comment.objects.get(author=request.user.username, pk=comment_num)
        res.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Comment.DoesNotExist:
        return redirect('login_home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'tutorial/register.html',
                          {'form': form})
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'],
                                            password=request.POST[
                                                'password1'])
            user.save()
            login(request, user)
            return redirect('login_home')
        else:
            return render(request, 'tutorial/register.html',
                          {'form': UserRegisterForm,
                           'error': 'Passwords do not match'})
    else:
        form = UserRegisterForm()
    return render(request, 'tutorial/register.html', {'form': form})


def like_handler(request,post_num:int,is_liked:int):
    current_post = Guide.objects.get(pk=post_num)
    new_post = deepcopy(current_post)
    if is_liked:
        new_post.likes_amount += 1
    else:
        new_post.likes_amount -= 1
    current_post.delete()
    new_post.save()
    for comment in Comment.objects.filter(to_post=post_num):
        comment1 = deepcopy(comment)
        comment1.to_post = new_post.pk
        comment.delete()
        comment1.save()
    for like in Like.objects.filter(to_post=post_num):
        like1 = deepcopy(like)
        like1.to_post = new_post.pk
        like.delete()
        like1.save()
    if is_liked:
        new_like = Like(username=request.user.username,to_post=new_post.pk)
        new_like.save()
    else:
        Like.objects.get(username=request.user.username,to_post=new_post.pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))
