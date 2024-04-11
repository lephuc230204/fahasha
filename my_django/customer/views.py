from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from .models import CartItem, Product, Cart
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Kiểm tra xem tài khoản đã tồn tại hay chưa
        if User.objects.filter(username=username).exists():
            error_message = "Tên đăng nhập đã tồn tại. Vui lòng chọn tên đăng nhập khác."
            return render(request, 'register.html', {'error_message': error_message})

        # Kiểm tra mật khẩu và xác nhận mật khẩu có khớp nhau hay không
        if password != confirm_password:
            error_message = "Mật khẩu và xác nhận mật khẩu không khớp."
            return render(request, 'register.html', {'error_message': error_message})

        # Tạo tài khoản mới
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Xác thực tài khoản và chuyển hướng trang
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')  # Chuyển hướng đến product-list
        else:
            error_message = "Tên đăng nhập hoặc mật khẩu không chính xác."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

# cấu hình cho view_home khi đăng nhập
def view_home(request):
    products = Product.objects.all() 
    return render(request, 'view_home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
    # return render(request, 'product_list.html')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    quantity = int(request.POST['quantity'])

    # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(customer=request.user)
    cart.products.remove(product)
    return redirect('cart')

@login_required
def cart(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = cart.cartitem_set.all()

    total_price = 0
    total_quantity = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        total_price += item.total_price
        total_quantity += item.quantity

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity
    }
    return render(request, 'cart.html', context)



def cart_summary(request):
    cart = Cart.objects.get(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    
    context = {
        'total_price': total_price,
        'total_quantity': total_quantity,
    }
    
    return render(request, 'cart_summary.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})