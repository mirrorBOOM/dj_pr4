from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Tag
from .forms import ProductForm, CategoryForm, TagForm


def product_list(request):
    products = Product.objects.filter(is_deleted=False)
    category_name = None
    tag_name = None

    category_id = request.GET.get('category')
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
            products = products.filter(category_id=category_id)
            category_name = category.name
        except Category.DoesNotExist:
            pass

    tag_id = request.GET.get('tag')
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
            products = products.filter(tags__id=tag_id)
            tag_name = tag.name
        except Tag.DoesNotExist:
            pass

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'category_name': category_name,
        'tag_name': tag_name,
    }
    return render(request, 'product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_deleted=False)

    # Получаем товары с теми же тегами
    related_products = Product.objects.filter(
        tags__in=product.tags.all(),
        is_deleted=False
    ).exclude(id=product.id).distinct()[:3]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})


def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = TagForm()

    return render(request, 'add_tag.html', {'form': form})