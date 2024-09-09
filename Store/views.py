from django.http import HttpResponse
from Cart.models import CartItem
from django.shortcuts import render, get_object_or_404
from .models import Product
from Category.models import Category
from Cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def store(request, category_slug=None):
    """
    View to display products in the store. Supports filtering by category and pagination.
    """
    # Initialize variables
    categories = None
    products = Product.objects.all().filter(is_available=True).order_by('id')  # Default to all available products

    # If a category slug is provided, filter products by category
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=categories)

    # Pagination setup (6 products per page)
    paginator = Paginator(products, 1)
    page = request.GET.get('page')

    try:
        paged_products = paginator.get_page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page.
        paged_products = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results.
        paged_products = paginator.page(paginator.num_pages)

    # Count of filtered products
    product_count = products.count()

    # Context for rendering
    context = {
        'products': paged_products,
        'product_count': product_count,
        'category': categories,  # Passing selected category for filtering info
    }

    return render(request, 'Store/store.html', context)


def product_detail(request, category_slug, product_slug):
    """
    View to display details of a single product.
    """
    # Fetch the product or return a 404 if not found
    single_product = get_object_or_404(
        Product.objects.select_related('category'),  # Using select_related for optimized query
        category__slug=category_slug, slug=product_slug
    )

    # Check if the product is already in the cart
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()

    # Context for rendering
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'Store/product_detail.html', context)


def search(request):
    products = []  # Default to an empty list
    product_count = 0  # Default count

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Use Q objects to filter based on multiple conditions
            products = Product.objects.filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            ).order_by('id')
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'Store/store.html', context)