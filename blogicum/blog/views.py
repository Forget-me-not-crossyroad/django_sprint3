from datetime import timezone
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from blog.models import Post, Category

# posts = [
#     {
#         'id': 0,
#         'location': 'Остров отчаянья',
#         'date': '30 сентября 1659 года',
#         'category': 'travel',
#         'text': '''Наш корабль, застигнутый в открытом море
#                 страшным штормом, потерпел крушение.
#                 Весь экипаж, кроме меня, утонул; я же,
#                 несчастный Робинзон Крузо, был выброшен
#                 полумёртвым на берег этого проклятого острова,
#                 который назвал островом Отчаяния.''',
#     },
#     {
#         'id': 1,
#         'location': 'Остров отчаянья',
#         'date': '1 октября 1659 года',
#         'category': 'not-my-day',
#         'text': '''Проснувшись поутру, я увидел, что наш корабль сняло
#                 с мели приливом и пригнало гораздо ближе к берегу.
#                 Это подало мне надежду, что, когда ветер стихнет,
#                 мне удастся добраться до корабля и запастись едой и
#                 другими необходимыми вещами. Я немного приободрился,
#                 хотя печаль о погибших товарищах не покидала меня.
#                 Мне всё думалось, что, останься мы на корабле, мы
#                 непременно спаслись бы. Теперь из его обломков мы могли бы
#                 построить баркас, на котором и выбрались бы из этого
#                 гиблого места.''',
#     },
#     {
#         'id': 2,
#         'location': 'Остров отчаянья',
#         'date': '25 октября 1659 года',
#         'category': 'not-my-day',
#         'text': '''Всю ночь и весь день шёл дождь и дул сильный
#                 порывистый ветер. 25 октября.  Корабль за ночь разбило
#                 в щепки; на том месте, где он стоял, торчат какие-то
#                 жалкие обломки,  да и те видны только во время отлива.
#                 Весь этот день я хлопотал  около вещей: укрывал и
#                 укутывал их, чтобы не испортились от дождя.''',
#     },
# ]


def index(request):
    post_list = Post.objects.select_related('category').filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, pk):
    template_name = 'blog/detail.html'
    post = get_object_or_404(
        Post.objects.filter(Q(is_published=True)
                            & Q(category__is_published=True)
                            & Q(pub_date__lt=timezone.now())
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
    category_posts = Post.objects.filter(
        is_published=True,
        pub_date_lt=timezone.now(),
        category=category
    )
    context = {'category': category, 'post_list': category_posts}
    return render(request, 'blog/category.html', context)
