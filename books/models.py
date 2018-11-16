from django.db import models

# Create your models here.
from db.base_model import BaseModel
from tinymce.models import HTMLField
from books.enums import *

class BooksManager(models.Manager):
    def get_books_by_type(self, type_id, limit=None, sort='default'):
        if sort == 'new':
            order_by = ('-create_time',)
        elif sort == 'hot':
            order_by = ('-sales',)
        elif sort == 'price':
            order_by = ('price',)
        else:
            order_by =('-pk',) # order by primary key
        books_li = self.filter(type_id=type_id).order_by(*order_by)

        if limit:
            books_li = books_li[:limit]

        return books_li

    def get_books_by_id(self, books_id):
        try:
            books = self.get(id=books_id)
        except self.model.DoesNotExist:
            books = None
        return books

class Books(BaseModel):
    books_type_choices = ((k, v) for k,v in BOOKS_TYPE.items())
    status_choices = ((k, v) for k,v in STATUS_CHOICE.items())
    type_id = models.SmallIntegerField(default=PYTHON, choices=books_type_choices, verbose_name='books category')
    name = models.CharField(max_length=20, verbose_name='books name')
    desc = models.CharField(max_length=128, verbose_name='books describe')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='books price')
    unit = models.CharField(max_length=20, verbose_name='books unit')
    stock = models.IntegerField(default=1, verbose_name='books stock')
    sales = models.IntegerField(default=0, verbose_name='sales of books')
    detail = HTMLField(verbose_name='detail of book')
    image = models.ImageField(upload_to='books', verbose_name='image of book')
    status = models.SmallIntegerField(default=ONLINE, choices=status_choices, verbose_name='status of book')

    objects = BooksManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 's_books'
        verbose_name = 'books'
        verbose_name_plural = verbose_name
