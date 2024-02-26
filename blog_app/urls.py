from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HomeView
from .views import ArticleView, ArticleCreateView, ArticleDraftView, ArticleDetailView, ArticleDeleteView
from .views import CommentCreateView, LikePostView
from .views import CreateUserView, CreateProfileView, ConfirmUserView, LoginView, LogoutView
from .views import ResetPassword, ForgotPassword
from .views import NewsList, UserDetailView, UserEditView

app_name = 'blog_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup', CreateUserView.as_view(), name='signup'),
    path('set_profile', CreateProfileView.as_view(), name='save_profile'),
    path('set_profile/<user_id>', CreateProfileView.as_view(), name='set_profile'),
    path('login', LoginView.as_view(), name='login'),
    path('confirm_email/', ConfirmUserView.as_view(), name='get_confirmation'),
    path('confirm_email/<encoded>', ConfirmUserView.as_view(), name='confirm_email'),
    path('user/<pk>', UserDetailView.as_view(), name='user_detail'),
    path('edit_profile', UserEditView.as_view(), name='edit_profile'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('articles', ArticleView.as_view(), name='articles'),
    path('new_article', ArticleCreateView.as_view(), name='new_article'),
    path('delete_post/<pk>', ArticleDeleteView.as_view(), name='delete_post'),
    path('news', NewsList.as_view(), name="news"),
    path('draft', ArticleDraftView.as_view(), name='drafts'),
    path('draft/<post_id>', ArticleDraftView.as_view(), name='draft'),
    path('article/<pk>', ArticleDetailView.as_view(), name='view_article'),
    path('comment', CommentCreateView.as_view(), name='comment'),
    path('like', LikePostView.as_view(), name='like'),
    path('forgot_password', ForgotPassword.as_view(), name='forgot_password'),
    path('reset_password', ResetPassword.as_view(), name='update_password'),
    path('reset_password/<encoded>', ResetPassword.as_view(), name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)