from django.urls import path,re_path
from . import views

app_name= "customer"

urlpatterns = [
    path('create-customer', views.create_customer, name='create_customer'),
    path('customer-list', views.customer_list, name='customer_list'),
    re_path(r'^delete-customer/(?P<pk>.*)/', views.delete_customer, name='delete_customer'),
    re_path(r'^update-customer/(?P<pk>.*)/', views.update_customer, name='update_customer'),
]
