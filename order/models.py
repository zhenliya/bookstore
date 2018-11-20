from django.db import models
from db.base_model import BaseModel
# Create your models here.

class OrderInfo(BaseModel):
    
    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "微信支付"),
        (3, "支付宝"),
        (4, "银联支付")
     )

    PAY_METHODS_ENUM = {
        "CASH": 1,
        "WEIXIN": 2,
        "ALIPAY": 3,
        "UNIONPAY": 4,
    }

    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
    )

    order_id = models.CharField(max_length=64,primary_key=True,verbose_name='order id')
    passport = models.ForeignKey('users.Passport',on_delete=True, verbose_name='user')
    addr = models.ForeignKey('users.Address', on_delete=True, verbose_name='address')
    total_count = models.IntegerField(default=1, verbose_name='book number')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='express price')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='total price')
    status = models.SmallIntegerField(choices=ORDER_STATUS_CHOICES,default=1,verbose_name='order status')
    pay_method = models.SmallIntegerField(choices=PAY_METHOD_CHOICES, default=1, verbose_name='pay method')
    trade_id = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='trade number')

    class Meta:
        db_table = 's_order_info'


class OrderBooks(BaseModel):
    order = models.ForeignKey('OrderInfo', on_delete=True, verbose_name='order id')
    books = models.ForeignKey('books.Books', on_delete=True, verbose_name='book id')
    count = models.IntegerField(default=1, verbose_name='book count')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='total price')

    class Meta:
        db_table = 's_order_books'
