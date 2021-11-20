from django.urls import path,re_path
from . import views


app_name = "product"
urlpatterns = [
    path('create-product', views.create_product, name='create_product'),
    path('list-products', views.product_list, name='product_list'),
    re_path(r'^delete-product/(?P<pk>.*)/', views.delete_product, name='delete_product'),
    re_path(r'^update-product/(?P<pk>.*)/', views.update_product, name='update_product'),

    path('create-quotation', views.create_quotation, name='create_quotation'),
    path('quotation-list', views.quotation_list, name='quotation_list'),
    re_path(r'^quotation-single/(?P<pk>.*)/', views.single_quotation, name='single_quotation'),
    re_path(r'^delete-quotation/(?P<pk>.*)/', views.delete_quotation, name='delete_quotation'),
    re_path(r'^update-quotation/(?P<pk>.*)/', views.update_quotation, name='update_quotation'),
]
