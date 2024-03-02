from django.views.generic import TemplateView
from blog_app.models import User
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render
from blog_app.models import News, Article

class HomeView(TemplateView):
    """view to render home page"""

    template_name = 'blog_app/index.html'

    def get(self, request):
        """handle get"""
        User.objects.filter(confirmed_email=False,
                            date_joined__lte=(timezone.now() -
                                              timedelta(days=30))).delete()
        query = News.objects.all().order_by('-created_at')
        articles = Article.objects.filter(publish_date__isnull=False) \
                                            .order_by('-publish_date')
        context = self.get_context_data()
        context['news'] = query[:3] if len(query) > 5 else query
        context['articles'] = articles[:3] if len(articles) > 3 else articles
        return render(request, self.template_name, context)

    