from blog.views import page_not_found_view
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('pages/', include('pages.urls', namespace='pages')),
]

handler404 = page_not_found_view
