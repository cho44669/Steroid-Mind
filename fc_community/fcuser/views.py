from django.shortcuts import render, redirect
# 비밀번호 암호화 저장, 비밀번호 체크
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser
from django.http import HttpResponse
from .forms import LoginForm
# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        # html에서 name 필드에 있는 값을 키로 해서 전달이 됨
        username = request.POST.get('username', None)  # request.POST 는 딕셔너리 형태
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re_password', None)

        res_data = {}

        if not (username and useremail and password and re_password):
            res_data['error'] = '모든 값을 입력해야 합니다.'
        # 비밀번호 확인
        elif password != re_password:
            res_data['error'] = '비밀번호가 다릅니다.'
        else:
            fcuser = Fcuser(  # fcuser 생성(클래스 가져오기)
                username=username,  # class변수 객체 생성
                useremail=useremail,
                password=make_password(password)
            )

            fcuser.save()  # DB 저장.

        return render(request, 'register.html', res_data)  # 페이지 전달할 때 데이터 전달.
