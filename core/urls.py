from django.urls import path
from . import views

urlpatterns=[
    path('core/', views.core, name='core'),
    path('products/', views.products, name='products'),
    path('products/delete/<int:pk>/', views.product_delete, name='products-delete'),
    path('products/detail/<int:pk>/', views.product_detail,name='products-detail'),
    path('products/edit/<int:pk>/', views.product_edit,name='products-edit'),
    path('clients/', views.clients, name='clients'),
    path('clients/detail/<int:pk>/', views.client_detail,name='client-detail'),
    path('orders/', views.order, name='orders'),
]