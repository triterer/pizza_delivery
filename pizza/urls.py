from django.urls import path

from pizza.views import create, view, close, stats

urlpatterns=[
path('/create', create, name='create_pizza'),
path('/view/(?P<pizza_order_id>[0-9]+)', view, name='view'),
path('/close/(?P<pizza_order_id>[0-9]+)', close, name='close'),
path('/stats', stats, name='stats'),
]