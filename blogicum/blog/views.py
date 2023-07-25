from datetime import datetime as dt
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from blog.models import Post, Category


def index(request):
    post_list = Post.objects.select_related('category', 'location').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=dt.now()
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(Q(is_published=True)
                            & Q(category__is_published=True)
                            & Q(pub_date__lt=dt.now())
                            ),
        pk=pk
    )
    context = {
        'post': post,
    }
    return render(request, template_name, context)


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(Q(is_published=True)),
        slug=category_slug
    )
    category_posts = Post.objects.select_related('category').filter(
        is_published=True,
        pub_date__lt=dt.now(),
        category=category
    )
    context = {'category': category, 'post_list': category_posts}
    return render(request, 'blog/category.html', context)
