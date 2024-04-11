from django.urls import path
from . import views

urlpatterns = [

    path('', views.view_home, name='customer'),

    path('register/', views.register),
    path('login/',    views.login_view, name = 'login' ),

    # path('products/', views.product_list, name='product_list'),
    # path('products/<int:product_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart, name='cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('cart/summary/', views.cart_summary, name='cart_summary'),

    path('product-list/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart-summary/', views.cart_summary, name='cart_summary'),
    path('product-detail/<int:product_id>', views.product_detail, name ='product_detail' )
]


    