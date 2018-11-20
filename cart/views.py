from django.shortcuts import render
from django.http import JsonResponse
from books.models import Books
from utils.decorators import login_required
# from django_redis import get_redis_connection
# from django_redis.client import DefaultClient
import redis 

# Create your views here.

@login_required
def cart_add(request):

    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    if not all([books_id, books_count]):
        return JsonResponse({'res':1, 'errmsg':'data no full'})

    books = Books.objects.get_books_by_id(books_id=books_id)

    if books is None:
        return JsonResponse({'res':2,'errmsg':'book is not exist'})

    try:
        count = int(books_count)

    except Exception as e:
        return JsonResponse({'res':3,'errmsg':'the count must be a digist'})

    conn = redis.Redis(host='localhost',port=6379)

   #conn = get_redis_connection("default")
    cart_key = 'cart_%d' %request.session.get('passport_id')

    res = conn.hget(cart_key, books_id)

    if res is None:
        res = count
    else:
        res = int(res) + count

    if res > books.stock:
        return JsonResponse({'res': 4, 'errmsg':'books not enough'})
    else:
        conn.hset(cart_key, books_id,res)

    return JsonResponse({'res':5})


@login_required
def cart_count(request):
    conn = redis.Redis(host='localhost',port=6379)
    cart_key = 'cart_%d' %request.session.get('passport_id')

    res = 0
    res_list = conn.hvals(cart_key)

    for i in res_list:
        res += int(i)

    return JsonResponse({'res':res})


@login_required
def cart_show(request):
    conn = redis.Redis(host='localhost', port=6379)
    cart_key = 'cart_%d' %request.session.get('passport_id')
    res_dict = conn.hgetall(cart_key)


    books_li = []
    total_count = 0
    total_price = 0

    for id, count in res_dict.items():
        books = Books.objects.get_books_by_id(books_id=id)
        books.count = int(count)
        books.amount = int(count) * books.price
        books_li.append(books)

        total_count += int(count)
        total_price += int(count) * books.price


    context = {
        'books_li': books_li,
         'total_count': total_count,
         'total_price': total_price,
          }
    return render(request, 'cart/cart.html', context)


@login_required
def cart_del(request):
    books_id = request.POST.get('books_id')
    print('~~~~books_id~~~`',books_id)
    if not books_id:
        return JsonResponse({'res': 1, 'errmsg':'data not enough'})

    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res':2 , 'errmsg':'book is not exsit'})

    conn = redis.Redis(host='localhost',port=6379)
    cart_key = 'cart_%d' %request.session.get('passport_id')
    conn.hdel(cart_key, books_id)

    return JsonResponse({'res': 3})


@login_required
def cart_update(request):
    books_id = request.POST.get('books_id')
    books_count = request.POST.get('books_count')

    if not all([books_id, books_count]):
        return JsonResponse({'res':1,'errmsg': 'data not enough'})
    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return JsonResponse({'res': 2, 'errmsg': 'book is not exist'})
    try:
        books_count = int(books_count)
    except Exception as e:
        return JsonResponse({'res':3, 'errmsg':'num must be a digist'})

    conn = redis.Redis(host='localhost', port=6379)
    cart_key = 'cart_%d' %request.session.get('passport_id')

    if books_count > books.stock:
        return JsonResponse({'res': 4, 'errmsg': 'books inventory shortage'})

    conn.hset(cart_key, books_id, books_count)
    return JsonResponse({'res': 5 })
