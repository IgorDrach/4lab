"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest
from app import forms, views
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Comment
from .forms import BlogForm, CommentForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Парк аттракционов',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ресурсы',
            'message':'Страница с полезными источниками',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'контакты',
            'message':'Контактные данные',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Тема',
            'message':'Страница с описанием вашего приложения.',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1':'Мужчина','2':'Женщина'}
    internet = {'1':'Каждый день','2':'Несколько раз в день','3':'Несколько раз в неделю','4':'Несколько раз в месяц'}
    if request.method == 'POST':
        form = forms.AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'да'
            else:
                data['notice'] == 'нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = forms.AnketaForm()

    return render(
        request,
        'app/anketa.html',
        {
        'form':form,
        'data':data
        }
     )

def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = UserCreationForm()
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform':regform,
            'year':datetime.now().year
            }
        )
def blog(request):
    posts = Blog.objects.all()
    
    assert isinstance(request,HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts':posts,
            'year':datetime.now().year,
            }
        )
def blogpost(request,parametr):
    assert isinstance(request,HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST

        form = CommentForm(request.POST)

        if form.is_valid():

            comment_f = form.save(commit=False)

            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя

            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату

            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий

            comment_f.save() # сохраняем изменения после добавления полей

            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:

        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1':post_1,
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
            }
        )
def newpost(request):
    assert isinstance(request,HttpRequest)
    
    if request.method == "POST":
        blogform = BlogForm(request.POST,request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit = False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()
            
            return redirect('blog')
    else:
        blogform = BlogForm()
    return render(
        request,
        'app/newpost.html',
        {
            'blogform':blogform,
            'title':'Добавить статью блога',
            'year': datetime.now().year,
            }
        )
def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Тема',
            'message':'ВИИИИДЕЕООО',
            'year':datetime.now().year,
        }
    )