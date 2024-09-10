from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from Store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'Cart/cart.html', context)


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('cart')


def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    # Handle variations if any
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(user=current_user, product=product)
    else:
        cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, product=product)

    # Update or create cart item
    if cart_items.exists():
        # Check for existing variations
        existing_variations = [list(item.variations.all()) for item in cart_items]
        if product_variation in existing_variations:
            index = existing_variations.index(product_variation)
            cart_item = cart_items[index]
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user if current_user.is_authenticated else None,
                cart=None if current_user.is_authenticated else cart
            )
            cart_item.variations.add(*product_variation)
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=current_user if current_user.is_authenticated else None,
            cart=None if current_user.is_authenticated else cart
        )
        cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'Store/checkout.html', context)
