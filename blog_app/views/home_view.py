from django.views.generic import TemplateView

class HomeView(TemplateView):
    """view to render home page"""

    template_name = 'blog_app/index.html'