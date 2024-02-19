from django.views.generic import TemplateView
from django.shortcuts import render
from blog_app.forms import LikeForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class LikePostView(TemplateView):
    """create a new comment"""


    def post(self, request):
        """post a comment"""

        user = request.POST.get('user')
        article = request.POST.get('article')
        
        data = {'user': user,
                'article': article}

        form = LikeForm(data)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        if not article:
            return HttpResponseRedirect(reverse('blog_app:home'))
        return HttpResponseRedirect(reverse('blog_app:view_article', args=[article]))
