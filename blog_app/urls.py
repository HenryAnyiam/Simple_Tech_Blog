from django.urls import path
from .views import HomeView
from .views import ArticleView, ArticleCreateView, ArticleDraftView, ArticleDetailView
from .views import CommentCreateView, LikePostView
from .views import CreateUserView, CreateProfileView, ConfirmUserView, LoginView, LogoutView

app_name = 'blog_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup', CreateUserView.as_view(), name='signup'),
    path('set_profile', CreateProfileView.as_view(), name='set_profile'),
    path('login', LoginView.as_view(), name='login'),
    path('confirm_email/', ConfirmUserView.as_view(), name='get_confirmation'),
    path('confirm_email/<encoded>', ConfirmUserView.as_view(), name='confirm_email'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('articles', ArticleView.as_view(), name='articles'),
    path('new_article', ArticleCreateView.as_view(), name='new_article'),
    path('draft', ArticleDraftView.as_view(), name='drafts'),
    path('draft/<post_id>', ArticleDraftView.as_view(), name='draft'),
    path('article/<pk>', ArticleDetailView.as_view(), name='view_article'),
    path('comment', CommentCreateView.as_view(), name='comment'),
    path('like', LikePostView.as_view(), name='like'),
]