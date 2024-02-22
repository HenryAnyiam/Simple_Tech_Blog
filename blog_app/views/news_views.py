from django.views.generic import TemplateView
from django.shortcuts import render
from blog_app.util_funcs import NewsScraper
from blog_app.models import News
from datetime import datetime, timedelta
from django.utils import timezone

NEWS_SCREAPER = NewsScraper()


class NewsList(TemplateView):

    template_name = 'blog_app/all_news.html'

    def get(self, request):
        """handle get"""
        context = self.get_context_data()
        query = News.objects.all().order_by('-created_at')
        if not query:
            NEWS_SCREAPER.update_news_db()
            query = News.objects.all().order_by('-created_at')
        elif query and ((query[0].created_at + timedelta(hours=12)) < 
            datetime.now(tz=timezone.utc)):
            NEWS_SCREAPER.update_news_db()
            query = News.objects.all().order_by('-created_at')

        print(query[0].created_at + timedelta(hours=12), datetime.now(tz=timezone.utc))
        
        if len(query) > 25:
            context['news'] = query[:25]
            context['next'] = 25
        else:
            context['news'] = query
        return render(request, self.template_name, context=context)

    def post(self, request):
        next = request.POST.get('next')
        context = self.get_context_data()
        query = News.objects.all().order_by('-created_at')
        prev = request.POST.get('prev')
        length = len(query)
        if next:
            try:
                next = int(next)
            except ValueError:
                next = 25 if length > 25 else length
            else:
                prev = next
                next = (next + 25)
                if length < next:
                    next = (length - prev) + prev
                    
        elif prev:
            try:
                prev = int(prev)
            except ValueError:
                prev = 0
            else:
                next = prev
                prev = prev - 25
                if prev < 0:
                    prev = 0
        query = query[prev:next]
        context['news'] = query
        context['prev'] = prev if prev != 0 else None
        context['next'] = next if next != length else None
        return render(request, self.template_name, context)
        
