from django import forms
from .models import User, Article, Comment

class UserSignUpForm(forms.ModelForm):
    """create a default form to create a new user"""

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    """create a form for further sign up"""

    class Meta:
        model = User
        fields = ['profile_pic', 'about']


class ArticleForm(forms.ModelForm):
    """create a form to create a new article"""

    class Meta:
        model = Article
        fields = ['title', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'posttitle'}),
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    """create a form for a new comment"""

    class Meta:
        model = Comment
        fields = ['comment']
