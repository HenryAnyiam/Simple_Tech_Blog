from django import forms
from .models import User, Article, Comment, Like, News

class UserSignUpForm(forms.ModelForm):
    """create a default form to create a new user"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password']
        
        widgets = {
            'password': forms.PasswordInput()
        }


class UserProfileForm(forms.ModelForm):
    """create a form for further sign up"""

    class Meta:
        model = User
        fields = ['profile_pic', 'about']

        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'})
        }


class ArticleForm(forms.ModelForm):
    """create a form to create a new article"""

    class Meta:
        model = Article
        fields = ['title', 'image', 'body', 'author']

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'posttitle'}),
        #     'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        #     'author': forms.HiddenInput(attrs={'value': ''})
        # }


class CommentForm(forms.ModelForm):
    """create a form for a new comment"""

    class Meta:
        model = Comment
        fields = ['article', 'user', 'comment']


class LikeForm(forms.ModelForm):
    """create a form to like a post"""

    class Meta:
        model = Like
        fields = ['user', 'article']


class NewsForm(forms.ModelForm):
    """create a form to create news objects"""

    class Meta:
        model = News
        fields = ['title', 'link', 'summary']
