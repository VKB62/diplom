from django.shortcuts import render, redirect
from .main_block import main
from .forms import UserForm
from .set import *


def vote(request):
    return render(request, 'main/home.html', {'title': 'Главная страница'})


def upload(request):
    main()
    return redirect('/login/')


def login(request):
    submitbutton = request.POST.get("submit")

    passw = ''
    emailvalue = ''

    form = UserForm(request.POST or None)
    if form.is_valid():
        passw = form.cleaned_data.get("passw")
        emailvalue = form.cleaned_data.get("email")
    flag = 0
    for i in users:
        if emailvalue == i:
            if users[i] == passw:
                flag = 1
    if flag == 1:
        context = {'form': form, 'passw': 'Успешная авторизация', 'submitbutton': submitbutton, 'emailvalue': emailvalue}
    else:
        context = {'form': form, 'passw': 'Неверный логин или пароль', 'submitbutton': submitbutton, 'emailvalue': emailvalue}

    return render(request, 'main/login.html', context)
