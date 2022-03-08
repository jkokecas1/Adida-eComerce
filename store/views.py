"""-----------------------------------------------------------------------------
:*
:* Archivo      :
:* Autor        :
:* Fecha        :
:* Descripcion  :
-----------------------------------------------------------------------------"""
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct

"""-----------------------------------------------------------------------------
:* Store
-----------------------------------------------------------------------------"""
def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        # Obtenemos todos los productos filtrados por la validez y ordenados por id
        products = Product.objects.all().filter(is_available=True).order_by('id')
        # Utilizamos la paginacion de los productos de 6 por pagina
        paginator = Paginator(products,6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    # Guardasmo los datos en context
    context = {
        'products':paged_products,
        'products_count':products_count,
    }
    return render(request, 'store/store.html',context)


"""-----------------------------------------------------------------------------
:* Product_detail
-----------------------------------------------------------------------------"""
def product_detail(request, category_slug, product_slug):
    try:
        # Obtenemos el productos con los requisitos espesificados
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        # Obtenemos los items del carrito sie xiste
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e

    # Si el usuario esta autenticado
    if request.user.is_authenticated:
        try:
            # Obtenemos la ordern si existe
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        # La vaiable se iguala a None
        orderproduct = None

    # Obtener Reviews: filtrando por id producto y sus estatus sea True
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    # Obtener la galeria del product: filtrada con el id del producto
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)
    # Colocamos las variables en un arreglo
    context = {
        'single_product'    : single_product,
        'in_cart'           : in_cart,
        'orderproduct'      : orderproduct,
        'reviews'           : reviews,
        'product_gallery'   : product_gallery,
    }
    # Retornamos a la direccion de detalles del producto con los datos de context
    return render(request,'store/product_detail.html',context)


"""-----------------------------------------------------------------------------
:* search
-----------------------------------------------------------------------------"""
def search(request):
    # Verificamos que el requiest.Get sea el 'keyword'
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        # Si exutsten datos
        if keyword:
            # Obtenemos el producto ordenado de menor a mayor segun la fecha de cracion
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            # Aplicamos un count para obtener el numero de productos
            products_count = products.count()
    # Guardamos los datos en context
    context ={
        'products':products,
        'products_count':products_count
    }
    # Enviamos los datos de context al html
    return render(request, 'store/store.html',context)


"""-----------------------------------------------------------------------------
:* submit_review
-----------------------------------------------------------------------------"""
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    # Requerimos que el metodo sea POST
    if request.method == 'POST':
        try:
            # Obtenemos las review por el id  y el producto
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            return redirect(url)
        except Exception as e:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject    = form.cleaned_data['subject']
                data.rating     = form.cleaned_data['rating']
                data.review     = form.cleaned_data['review']
                data.ip         = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id    = request.user.id
                data.save()
                messages.surccess(request, 'Thank you')
                return redirect(url)
