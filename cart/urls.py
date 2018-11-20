from django.urls import path
from cart import views

app_name = "cart"

urlpatterns=[
    path('add/',views.cart_add, name='add'),
    path('count/',views.cart_count, name='count'),
    path('del/', views.cart_del, name='delete'),
    path('update/', views.cart_update, name='update'),
    path('',views.cart_show, name='show'),
    ]
