from datetime import datetime as dt
from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category

DISPLAYED_POSTS_NUMBER = 5


def index(request):
    """Функция для отображения главной страницы.
    Отображает 5 последних постов. Отображаются
    следующие атрибуты поста: время публикации,
    автор, локация, категория, заголовок (первые
    10 символов)"""
    # Запрос на получение постов, которые опубликованы не
    # позже момента запроса и имеют опубликованную категорию
    post_list = Post.objects.select_related('category', 'location').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.now()
    ).order_by('-pub_date')[:DISPLAYED_POSTS_NUMBER]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    """Функция для отображения детальной информации поста.
     Отображаются следующие атрибуты поста: время публикации,
    автор, локация, категория, заголовок"""
    template_name = 'blog/detail.html'
    # Запрос на получение поста по id, который опубликован не
    # позже момента запроса и имеет опубликованную категорию.
    # Возвращает 404 ошибку при невыполнении условий
    post = get_object_or_404(
        Post.objects.filter(is_published=True,
                            category__is_published=True,
                            pub_date__lt=dt.now()
                            ),
        pk=pk
    )
    context = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    """Функция для отображения постов,
    относящихся к выбранной категории. Отображаются
    следующие атрибуты поста: время публикации,
    автор, локация, категория, заголовок (первые
    10 символов)"""
    # Запрос на получение категории, соответствующей
    # выбранному slug и опубликованы
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    # Запрос на получение постов по выбранной категории, которые
    # опубликованы не позже момента запроса
    category_posts = Post.objects.select_related('category').filter(
        is_published=True,
        pub_date__lt=dt.now(),
        category=category
    )
    context = {'category': category, 'post_list': category_posts}
    return render(request, 'blog/category.html', context)
