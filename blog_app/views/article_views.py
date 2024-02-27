from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, DeleteView
from blog_app.models import User, Article
from blog_app.forms import ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

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
        image = request.FILES.get('image')
        body = request.POST.get('body')
        author = request.POST.get('author')
        form_data = {'title': title,
                    'body': body, 'author': author}
        
        form = ArticleForm(form_data)
        if form.is_valid():
            article = form.save(commit=False)
            if image:
                article.image = image
                article.get_thumbnail()
            article.save()
            url = reverse('blog_app:draft', kwargs={'post_id': article.id})
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
        drafts = Article.objects.filter(author=request.user, publish_date__isnull=True) \
                                .order_by('created_date')
        if not post_id:
            context['drafts'] = drafts
            if not drafts:
                context['message'] = "You currently have no saved drafts"
            return render(request, self.template_name, context=context)
        if post and request.user.id == post[0].author.id:
            context['post'] = post[0]
        else:
            return HttpResponseRedirect(reverse('blog_app:home'))
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
                post.get_thumbnail()
                post.publish_article()
                return HttpResponseRedirect(reverse('blog_app:view_article', args=[post.id]))
            elif edit == 'True':
                context = self.get_context_data()
                context['post'] = post
                context['edit'] = edit
                return render(request, self.template_name, context=context)
            elif draft == 'True':
                image = request.FILES.get('image')
                title = request.POST.get('title')
                body = request.POST.get('body')
                author = post.author
                form_data = {'title': title,
                            'body': body, 'author': author}
                form = ArticleForm(form_data)
                if form.is_valid():
                    if image:
                        post.clear_older_images()
                        post.image = image
                    post.get_thumbnail()
                    post.title = title
                    post.body = body
                    if image:
                        post.image = image
                    post.save()
                    post.get_thumbnail()
                    post.save()
                return HttpResponseRedirect(reverse('blog_app:draft', args=[post.id]))
            elif delete == 'True':
                post.delete()
                return HttpResponseRedirect(reverse('blog_app:drafts'))
        return HttpResponseRedirect(reverse('blog_app:home'))      


class ArticleView(TemplateView):
    """view articles"""

    template_name = 'blog_app/all_posts.html'
    
    def get(self, request):
        context = self.get_context_data()
        context['articles'] = Article.objects.filter(publish_date__isnull=False) \
                                            .order_by('-publish_date')
        context['users'] = User.objects.values_list('username', flat=True)
        context['error'] = None
        if not context['articles']:
            context['error'] = 'No articles found'
        else:
            if len(context['articles']) > 15:
                context['articles'] = context['articles'][:15]
                context['next'] = 15
        return render(request, self.template_name, context=context)

    def post(self, request):
        order_by = request.POST.get('order_by', 'publish_date')
        context = self.get_context_data()
        order = request.POST.get('order', '-')
        author = request.POST.get('author')
        error = None
        next = request.POST.get('next')
        prev = request.POST.get('prev')
        if next or prev:
            sort = request.POST.get('sort')
            sort = tuple(sort.split(',')) if sort else ('publish_date', '', '')
            order_by, order, author = sort
        if order == "descending" or order == '-':
            order = '-'
        else:
            order = ''
        if author:
            if order_by == 'publish_date' or order_by == 'views':
                context['articles'] = Article.objects \
                                        .filter(author__username=author, publish_date__isnull=False) \
                                        .order_by(order + order_by)
            elif order_by == 'likes' or order_by == 'comments':
                context['articles'] = Article.objects \
                                        .filter(author__username=author, publish_date__isnull=False) \
                                        .annotate(count_value=Count(order_by)). \
                                        order_by(order + 'count_value')
            else:
                context['articles'] = Article.objects \
                                        .filter(author__username=author, publish_date__isnull=False)
            error = f"No Article for Author named {author}" if not context['articles'] else None
        elif order_by:
            if order_by == 'publish_date' or order_by == 'views':
                context['articles'] = Article.objects \
                                             .filter(publish_date__isnull=False)\
                                             .order_by(order + order_by)
            elif order_by == 'likes' or order_by == 'comments':
                context['articles'] = Article.objects.filter(publish_date__isnull=False) \
                                        .annotate(count_value=Count(order_by)) \
                                        .order_by(order + 'count_value')
        context['error'] = error
        context['users'] = User.objects.values_list('username', flat=True)
        context['sort'] = f"{order_by},{order},{author}"
        if not context.get('articles'):
            context['error'] = 'No articles found'
        else:
            length = len(context['articles'])
            if next:
                try:
                    next = int(next)
                except ValueError:
                    next = 1 if length > 15 else length
                else:
                    prev = next
                    next = (next + 15)
                    if length < next:
                        next = (length - prev) + prev
                        
            elif prev:
                try:
                    prev = int(prev)
                except ValueError:
                    prev = 0
                else:
                    next = prev
                    prev = prev - 15
                    if prev < 0:
                        prev = 0
            else:
                prev, next = 0, 15 if len(context['articles']) >= 15 else len(context['articles'])
            context['articles'] = context['articles'][prev:next]
            context['prev'] = prev if prev != 0 else None
            context['next'] = next if next != length else None
        return render(request, self.template_name, context=context)           


class ArticleDetailView(DetailView):
    """View particular article"""

    model = Article
    template_name = 'blog_app/article.html'
    context_object_name = 'article'


class ArticleDeleteView(LoginRequiredMixin, DeleteView):

    login_url = '/login/'
    redirect_field_name = 'blog_app/post_draft.html'

    model = Article
    
    def get_success_url(self) -> str:
        return reverse('blog_app:articles')
