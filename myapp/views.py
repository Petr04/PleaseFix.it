from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from myapp.models import Problem

# Create your views here.

def index(request):
	pars_no_username = {k: v for k, v in list(request.GET.items())[1:]}
	if request.GET.get('username', '') != '':
		probs = Problem.objects.filter(
			user=User.objects.filter(username=request.GET['username'])[0],
			**pars_no_username
		)
	else:
		probs = Problem.objects.filter(**pars_no_username)

	if probs.count() == 0:
		return render(
			request, 'no_problems.html',
			{'title': 'Все жалобы', 'user': request.user}
		)

	return render(
		request, 'index.html',
		{
			'title': 'Все жалобы',
			'user': request.user,
			'probs': probs,
			'status_variants': Problem.status_variants,
		}
	)

def new(request):
	if request.method == 'GET':
		return render(request, 'new.html')

	if request.method == 'POST':
		prob = Problem(
			title=request.POST['title'],
			user=request.user,
			room=request.POST['room'],
			text=request.POST['text'],
			status='new'
		)
		prob.save()

		return redirect('/')

def register(request):
	if request.method == 'GET':
		return render(
			request, 'register.html',
			{'title': 'Регистрация', 'user': request.user}
		)

	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		pass_rep = request.POST.get('pass_rep', '')

		if '' in (username, password, pass_rep):
			messages.add_message(request, messages.ERROR, 'Заполните все поля')
			return redirect('/register')

		if password != pass_rep:
			messages.add_message(request, messages.ERROR, 'Пароли не совпадают')
			return redirect('/register')

		if User.objects.filter(username=username).exists():
			messages.add_message(request, messages.ERROR, 'Логин занят')
			return redirect('/register')

		user = User.objects.create_user(username=username, password=password)
		user.save()

		login(request, user)

		return redirect('/')

def login_page(request):
	if request.method == 'GET':
		return render(request, 'login.html', {'title': 'Вход', 'user': request.user})

	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')

		if '' in (username, password):
			messages.add_message(request, messages.ERROR, 'Заполните все поля')
			return redirect('/login')

		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.add_message(request, messages.ERROR, 'Неверный логин или пароль')
			return redirect('/login')

def logout_page(request):
	logout(request)
	return redirect('/')
