from django.views.generic import TemplateView
from django.shortcuts import render
from blog_app.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class CommentCreateView(TemplateView):
    """create a new comment"""


    def post(self, request):
        """post a comment"""

        comment = request.POST.get('comment')
        user = request.POST.get('user')
        article = request.POST.get('article')
        
        data = {'comment': comment, 'user': user,
                'article': article}

        form = CommentForm(data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog_app:view_article', args=[article]))
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('blog_app:home'))
