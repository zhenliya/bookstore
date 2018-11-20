from django.shortcuts import render,redirect,reverse
import re
from django.http import JsonResponse
from .models import Passport, Address
from utils.decorators import login_required

# Create your views here.

def register(request):
    return render(request, 'users/register.html')

def login(request):
    return render(request, 'users/login.html')

def register_handle(request):
     username = request.POST.get('user_name')
     password = request.POST.get('pwd')
     email = request.POST.get('email')

     if not all([username, password, email]):
         return render(request, 'users/register.html', {'errmsg':"It can't be null"})
     if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
         return render(request, 'users/register.html', {'errmsg':'The email is invalidate'})
     try:
         Passport.objects.add_one_passport(username=username, email=email, password=password)
     except:
         return render(request, 'users/register.html', {'errmsg':'username is exist'})
     return redirect(reverse('books:index'))

def login_check(request):
    print('++++++++login_check')
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    print('++++++++username.password.remember+++++',username,password,remember)

    if not all([username, password]):
        
        return JsonResponse({'res': 2})

    passport = Passport.objects.get_one_passport(username=username, password=password)
    print('++++++++passport+++++',passport)
    if passport:
        next_url = reverse('books:index')
        jires = JsonResponse({'res':1, 'next_url':next_url})

        if remember == 'true':
            print('++++++++++++cheked+++++++++++',remember)  
            jires.set_cookie('username', username, max_age=7*24*3600)
        else:
            print('+++++++++++remember++++++++++',remember)
            jires.delete_cookie('username')

        request.session['islogin'] = True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        print('++++++++request.islogin++++++++',request.session['islogin'])
        print ('+++++++jires++++++',jires)
        return jires
    else:
        print('00000000000000000')
        return JsonResponse({'res': 0})
     
def logout(request):
    request.session.flush()
    return redirect(reverse('books:index'))

@login_required
def user(request):
    ''' 
      user center messages
   '''
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)

    books_li = []

    context = {
        'addr': addr,
        'page': 'user',
        'books_li': books_li
   }
    return render(request, 'users/user_center_info.html', context)
