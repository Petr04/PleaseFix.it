from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from myapp.models import Problem, UserProfile

# Create your views here.

def index(request):
	if request.GET.get('toggle', '') != '':
		prob = Problem.objects.get(pk=request.GET['toggle'])
		if prob.status == 'new':
			prob.fixer = request.user
			prob.status = 'solving'
		else:
			prob.status = 'solved'
		prob.save()

		return redirect('/')

	pars_keywords = {}
	pars_user = {}
	for k, v in list(request.GET.items()):

		if v:
			if k not in ('user', 'fixer'):
				pars_keywords[k] = v
			else:
				pars_user[k] = v


	user_keywords = {}
	for k, v in pars_user.items():

		users = User.objects.filter(username=pars_user[k])
		if users.count() == 0:
			messages.add_message(request, messages.ERROR, 'Нет такого пользователя')
			return redirect('/')
		else:

			user_keywords[k] = users[0]


	probs = Problem.objects.filter(
		**pars_keywords,
		**user_keywords
	)

	if probs.count() == 0:
		return render(
			request, 'no_problems.html',
			{'title': 'Все жалобы', 'user': request.user}
		)

	admin = False
	if request.user.is_authenticated:
		profiles = UserProfile.objects.filter(user=request.user, admin=True)

		if profiles.count() != 0:
			admin = True

	return render(
		request, 'index.html',
		{
			'title': 'Все жалобы',
			'user': request.user,
			'status_variants': Problem.status_variants,
			'probs': probs,
			'admin': admin,
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

		user_profile = UserProfile(user=user, admin=False)

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
