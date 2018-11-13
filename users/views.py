from django.shortcuts import render,redirect,reverse
import re
from .models import Passport

# Create your views here.

def register(request):
    return render(request, 'user/register.html')


def register_handle(request):
     username = request.POST.get('user_name')
     password = request.POST.get('pwd')
     email = request.POST.get('email')

     if not all([username, password, email]):
         return render(request, 'users/register.html', {'errmsg':"It can't be null")

     if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
         return render(request, 'users/register.html', {'errmsg':'The email is invalidate'})

     try:
         Passport.objects.add_one_passport(username=username, email=email, password=password)
     except:
         return render(request, 'users/register.html', {'errmsg':'username is exist'})

     return redirect(reverse('user:register'))
