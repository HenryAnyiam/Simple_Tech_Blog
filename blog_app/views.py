from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .models import User, Article
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count

# Create your views here.

class HomeView(TemplateView):
    """view to render home page"""

    template_name = 'blog_app/index.html'


@method_decorator(login_required, name='dispatch')
class ArticleCreateView(CreateView):
    """render page to create a new post"""

    model = Article
    fields = '__all__'
    template_name = 'base_app/new_post.html'


class ArticleView(TemplateView):
    """view articles"""

    template_name = 'blog_app/all_posts.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['articles'] = []
        return context
    
    def get(self, request):
        context = self.get_context_data()
        context['article'] = Article.objects.order_by('publish_date')
        context['users'] = User.objects.values_list('username', flat=True)
        context['error'] = None
        if not context['articles']:
            context['error'] = 'No articles found'
        return render(request, self.template_name, context=context)

    def post(self, request):
        order_by = request.POST.get('order_by', 'publish_date')
        context = self.get_context_data()
        order = request.POST.get('order', '')
        author = request.POST.get('author')
        error = None
        if order == "descending":
            order = '-'
        else:
            order = ''
        if author:
            if order == 'publish_date' or order == 'views':
                context['articles'] = Article.objects \
                                        .filter(author__username=author) \
                                        .order_by(order + order_by)
            elif order == 'likes' or order == 'comments':
                context['articles'] = Article.objects \
                                        .filter(author__username=author) \
                                        .annotate(count_value=Count(order_by)). \
                                        order_by(order + 'count_value')
            error = f"No Article for Author named {author}" if not context['articles'] else None
        elif order_by:
            if order == 'publish_date' or order == 'views':
                context['articles'] = Article.objects \
                                        .order_by(order + order_by)
            elif order == 'likes' or order == 'comments':
                context['articles'] = Article.objects \
                                        .annotate(count_value=Count(order_by)). \
                                        order_by(order + 'count_value')
        context['error'] = error
        context['users'] = User.objects.values_list('username', flat=True)
        if not context['articles']:
            context['error'] = 'No articles found'
        return render(request, self.template_name, context=context)           
