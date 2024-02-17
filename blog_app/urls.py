from django.urls import path
from .views import HomeView, ArticleView, ArticleCreateView, ArticleDraftView, ArticleDetailView

app_name = 'blog_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('articles', ArticleView.as_view(), name='articles'),
    path('new_article', ArticleCreateView.as_view(), name='new_article'),
    path('draft', ArticleDraftView.as_view(), name='drafts'),
    path('draft/<post_id>', ArticleDraftView.as_view(), name='draft'),
    path('article/<pk>', ArticleDetailView.as_view(), name='view_article'),
]