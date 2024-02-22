from django.views.generic import TemplateView
from blog_app.models import User
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render

class HomeView(TemplateView):
    """view to render home page"""

    template_name = 'blog_app/index.html'

    def get(self, request):
        """handle get"""
        User.objects.filter(confirmed_email=False,
                            date_joined__lte=(timezone.now() -
                                              timedelta(days=30))).delete()
        return render(request, self.template_name)

    