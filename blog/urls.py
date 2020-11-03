from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='blog_index'),    # http://127.0.0.1/blog/
    path('<int:blog_id>/', views.detail, name='blog_detail'),
    path('archives/<int:year>/<int:month>/', views.archives, name='blog_archives'),
    # path('category/<int:category_id>/', views.category, name='blog_category'),
    path('tag/', views.tag, name='blog_tag'),
    path('column/<int:column_id>/', views.column, name='blog_column'),
    path('search/', views.search, name='blog_search'),
    path('article-create/', views.article_create, name='article_create'),
    path('article-safe-delete/<int:id>/', views.article_safe_delete, name='article_safe_delete'),
    path('article-update/<int:id>/', views.article_update, name='article_update'),
    path('increase-likes/<int:id>/', views.IncreaseLikesView.as_view(), name='increase_likes'),
]
