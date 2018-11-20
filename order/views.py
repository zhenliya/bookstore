from django.shortcuts import render,reverse, redirect
from django_redis import get_redis_connection
from django.db import transaction
from django.http import JsonResponse, HttpResponse

from users.models import Address
from books.model import Books
from order.models import OrderInfo, OrderBooks
from datetime import datetime
import os
import time


# Create your views here.
@login_required
def order_place(request):
    books_ids = request.POST.getlist('books_ids')

    if not books_ids:
        return redirect(reverse('cart:show')

    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)

    books_li = []
    total_count = 0
    total_price = 0

    conn = get_redis_connection('default')
    cart_key = 'cart_%d' %passport_id

    for id in books_ids:
        books = Books.objects.get_books_by_id(books_id=id)

        count = conn.hget(cart_key, id)

        amount = int(count) * books.price
        books.amount = amount
        books_li.append(books)
        total_count += int(count)
        total_price += books.amount

    transit_price = 10
    total_pay = total_price + transit_price

    books_ids =','.join(books_ids)
    context = {
        'addr': addr,
        'books_li': books_li,
        'total_count': total_count,
        'tarnsit_price': transit_price,
        'total_price': total_price,
        'total_pay': total_pay,
        'books_ids': books_ids,
        )
                        

        return render(request, 'order/place_order.html', context)
                        
@transaction.atomic
def order_commit(request):
    if not request.session.has_key('islogin'):
        return JsonResponse({'res': 0, 'errmsg':'you need login')

    addr_id = request.POST.get('addr_id')
    pay_method = request.Post.get('pay_method')
    books_ids = request.POST.get('books_ids')

    if not all([addr_id, pay_method, books_ids]):
        return JsonResponse({'res': 1, 'errmsg':'data not enough'})
    try:
        addr = Address.objects.get(id=addr_id)
    except Exception as e:
        return JsonResponse({'res': 2,'errmsg':'address mistake'})
    if int(pay_method) not in OrderOnfo.PAY_METHODS_ENUM.values():
        return JsonResponse('res': 3, 'errmsg': 'the pay method is not supported'})

    passport_id = request.session.get('passport_id')
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(passport_id)
    transit_price = 10
    total_count = 0
    total_price =0
    sid = transaction.savepoint()
    try:
        order = OrderInfo.objects.create(order_id= id,
                                         passport_id = passport_id,
                                         addr_id = addr_id,
                                         total_count = total_count,
                                         total_price = total_price,
                                         transit_price = transit_price,
                                         pay_method = pay_method)
        books_ids = books_ids.split(',')
        conn = get_redis_connection('default')
        cart_key = 'cart_%d' %passport_id

        for id in books_id:
            books = Books.objects.get_books_by_id(books_id=id)
            if books is None:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res':4, 'errmsg':'books information mistake'})

            count = conn.hget(cart_key, id)
            if int(count) > books.stock:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 5, 'errmsg': 'stock short')
            OrderBooks.objects.create(order_id = order_id,
                                      books_id = id,
                                      count = count,
                                      price = books.price)

            books.sales += int(count)
            books.stock -= int(count)
            books.save()

            total_count += int(count)
            total_price += in(count)* books.price
        order.total_count = total_count
        order.total_price = total_price
        order.save()
    except Exception as e:
        print('e:',e)
        transaction.savepoint_rollback(sid)
        return JsonResponse({'res':7, 'errmsg':'server error'})
    conn.hdel(cart_key, *books_ids)
    transaction.savepoint_commit(sid)
    return Jsonresponse({'res':6})
                                         
