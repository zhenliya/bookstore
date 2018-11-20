from django.conf.urls import url
from order import views


app_name = 'order'


urlpatterns=[
    path('place/', views.order_place, name='place'),
    path('commit/', views.order_commit, name='commit'),
    ]
