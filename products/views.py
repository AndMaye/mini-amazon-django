from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import render, redirect

def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        request.session['cart'] = {}
        return render(request, 'products/success.html')

    return render(request, 'products/checkout.html')

def product_list(request):
    products = Product.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    return render(request, 'products/product_list.html', {
        'products': products,
        'cart_count': cart_count
    })
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session['cart'] = cart
    return redirect('product_list')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_detail')
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] -= 1

        if cart[str(product_id)] <= 0:
            del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    return render(request, 'products/cart.html', {'cart': cart})

def cart_detail(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total
        
    })