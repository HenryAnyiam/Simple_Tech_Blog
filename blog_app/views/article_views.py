from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from blog_app.models import User, Article
from blog_app.forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

class ArticleCreateView(LoginRequiredMixin, TemplateView):
    """View To create a new article"""

    login_url = '/login/'
    redirect_field_name = 'blog_app/new_post.html'

    template_name = 'blog_app/new_post.html'

    def get(self, request):
        """Render form for the creation of a new article"""
        return render(request, self.template_name)
    
    def post(self, request):
        """Get data from user form to create a new article"""
        title = request.POST.get('title')
        image = request.POST.get('image')
        body = request.POST.get('body')
        author = request.POST.get('author')
        form_data = {'title': title, 'image': image,
                    'body': body, 'author': author}

        form = ArticleForm(form_data)
        if form.is_valid():
            user = form.save()
            url = reverse('blog_app:draft', kwargs={'post_id': user.id})
            return HttpResponseRedirect(url)
        else:
            context = self.get_context_data()
            context['error'] = form.errors
            context.update(**form_data)
            return render(request, self.template_name, context=context)


class ArticleDraftView(LoginRequiredMixin, TemplateView):
    """Handle Article drafts
    This includes viewing all saved drafts
    Viewing a single draft
    Editing a draft and
    Publishing or Deleting a draft"""

    login_url = '/login/'
    redirect_field_name = 'blog_app/post_draft.html'

    template_name = 'blog_app/post_draft.html'

    def get(self, request, post_id=None):
        """handle get request for article post"""
        post = Article.objects.filter(id=post_id)
        context = self.get_context_data()
        drafts = Article.objects.filter(author=request.user, publish_date__isnull=True)
        if not post_id:
            context['drafts'] = drafts
            if not drafts:
                context['message'] = "No Drafts Currently"
            return render(request, self.template_name, context=context)
        if post and request.user.id == post[0].author.id:
            context['post'] = post[0]
        else:
            error = "You have been redirected because you requested a page you do not have access to"
            return render(request, 'blog_app/index.html', {'error': error})
        return render(request, self.template_name, context=context)
    
    def post(self, request):
        """handle post request for article post"""
        publish = request.POST.get('publish')
        draft = request.POST.get('draft')
        edit = request.POST.get('edit')
        delete = request.POST.get('delete')
        post = request.POST.get('post')
        post = Article.objects.filter(id=post)
        if post:
            post = post[0]
            if publish == 'True':
                post.publish_article()
                success = "Post Published Successfully"
                return render(request, 'blog_app/index.html', {'success': success})
            elif edit == 'True':
                context = self.get_context_data()
                context['post'] = post
                context['edit'] = edit
                return render(request, self.template_name, context=context)
            elif draft == 'True':
                image = request.POST.get('image')
                title = request.POST.get('title')
                body = request.POST.get('body')
                author = post.author
                form_data = {'title': title, 'image': image,
                            'body': body, 'author': author}
                form = ArticleForm(form_data)
                if form.is_valid():
                    if image:
                        post.image = image
                    post.title = title
                    post.body = body
                    post.save()
                return HttpResponseRedirect(reverse(f'blog_app:draft', args=[post.id]))
            elif delete == 'True':
                post.delete()
                return HttpResponseRedirect(reverse(f'blog_app:drafts'))
        error = 'Unknown Error'
        return render(request, 'blog_app/index.html', {'error': error})     


class ArticleView(TemplateView):
    """view articles"""

    template_name = 'blog_app/all_posts.html'
    
    def get(self, request):
        context = self.get_context_data()
        context['articles'] = Article.objects.filter(publish_date__isnull=False) \
                                            .order_by('publish_date')
        context['users'] = User.objects.values_list('username', flat=True)
        context['error'] = None
        print(context)
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
                                        .filter(author__username=author, publish_date__isnull=False) \
                                        .order_by(order + order_by)
            elif order == 'likes' or order == 'comments':
                context['articles'] = Article.objects \
                                        .filter(author__username=author, publish_date__isnull=False) \
                                        .annotate(count_value=Count(order_by)). \
                                        order_by(order + 'count_value')
            else:
                context['articles'] = Article.objects \
                                        .filter(author__username=author, publish_date__isnull=False)
            error = f"No Article for Author named {author}" if not context['articles'] else None
        elif order_by:
            if order == 'publish_date' or order == 'views':
                context['articles'] = Article.objects \
                                        .order_by(order + order_by)
            elif order == 'likes' or order == 'comments':
                context['articles'] = Article.objects.filter(publish_date__isnull=False) \
                                        .annotate(count_value=Count(order_by)) \
                                        .order_by(order + 'count_value')
        context['error'] = error
        context['users'] = User.objects.values_list('username', flat=True)
        if not context.get('articles'):
            context['error'] = 'No articles found'
        return render(request, self.template_name, context=context)           


class ArticleDetailView(DetailView):
    """View particular article"""

    model = Article
    template_name = 'blog_app/article.html'
    context_object_name = 'article'
