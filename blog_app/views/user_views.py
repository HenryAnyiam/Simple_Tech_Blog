from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, View
from blog_app.models import User
from blog_app.forms import UserSignUpForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from blog_app.util_funcs import UtilClass
from django.http import HttpResponseRedirect

UTILS = UtilClass()

class CreateUserView(TemplateView):

    template_name = 'blog_app/signup.html'

    def get(self, request):
        """get page"""
        form = UserSignUpForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """get user submitted data"""
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(first_name=request.POST.get('first_name'),
                            last_name=request.POST.get('last_name'),
                            email=request.POST.get('email'),
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
            new_user.save()
            return HttpResponseRedirect(reverse('blog_app:set_profile', kwargs={'user_id': new_user.id}))
        else:
            return render(request, self.template_name, {'error': form.errors})


class CreateProfileView(TemplateView):

    template_name = 'blog_app/profile_setup.html'

    def get(self, request, user_id=None):
        """get page"""
        user = User.objects.filter(id=user_id)
        
        if not user:
            return reverse('blog_app:home')
        profile_form = UserProfileForm()
        user = user[0]
        UTILS.confirm_email(request, user.id, user.email)
        message = f"Confirmation Link sent to {user.email}."
        message += "Please check your Spam Folder if you don't see it in your Inbox"
        return render(request, self.template_name,
                      {'profile_form': profile_form,
                       'user_id': user_id,
                       'message': message})
    
    def post(self, request, user_id=None):
        """post user info"""
        user = User.objects.filter(id=user_id)
        if not user:
            return reverse('blog_app:home')
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            user = user[0]
            user.profile_pic = request.POST.get('profile_pic')
            user.about = request.POST.get('about')
            user.save()
            success = "User Profile Completed"
            return render(request, 'blog_app/login.html', {'success': success})
        else:
            error = profile_form.errors
            return render(request, self.template_name,
                          {'profile_form': profile_form,
                           'user_id': user_id,
                           'error': error})


class ConfirmUserView(TemplateView):

    template_name ='blog_app/confirm_email.html'

    def get(self, request, encoded=None):
        """View To confirm user email"""
        decode = UTILS.decode(encoded)
        if decode.get('error'):
            error = "Confirmation Link Expired"
            return render(request, self.template_name, {'error': error})
        user = User.objects.filter(id=decode.get('user_id'))
        if not user:
            error = "User Not Found Error. Click to resend Confirmation Email"
            return render(request, self.template_name, {'error': error})
        user = user[0]
        user.confirm_email()
        return HttpResponseRedirect(reverse('blog_app:login'))
    
    def post(self, request):
        """resend confirmation email"""

        email = request.POST.get('email')
        if not email:
            error = "Please Input Your Email"
            return render(request, self.template_name, {'error': error})
        user = User.objects.filter(email=email)
        if not user:
            error = "User Not Found Error. Click to resend Confirmation Email"
            return render(request, self.template_name, {'error': error})
        user = user[0]
        UTILS.confirm_email(request, user.id, user.email)
        success = "Confirmation Link Sent. Please Check You Spam if its not in your Inbox"
        return render(request, self.template_name, {'success': success})
    
class LoginView(TemplateView):

    template_name = 'blog_app/login.html'

    def get(self, request):
        """get page for login"""

        return render(request, self.template_name)
    
    def post(self, request):
        """log a user in"""

        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not username or not password:
            error = "Please Input Username/Email and Password"
            return render(request, self.template_name, {'error': error})
        user = authenticate(request, username=username, password=password)
        print(user)
        if not user:
            user = User.objects.filter(username=username)
            if not user:
                user = User.objects.filter(email=username)
                if not user:
                    error = "User does not exist. Check Username/Email"
                    return render(request, self.template_name, {'error': error})
                else:
                    error = "Incorrect Password"
                    return render(request, self.template_name, {'error': error})
            else:
                error = "Incorrect Password"
                return render(request, self.template_name, {'error': error})
        else:
            if user.confirmed_email:
                login(request, user, backend="blog_app.auth.CustomUserAuth")
                return HttpResponseRedirect(reverse('blog_app:home'))
            else:
                error = "Please Confirm Your Email Address"
                return render(request, self.template_name, {'error': error})


class LogoutView(View):

    def get(self, request):
        """log a user out"""
        if request.user:
            logout(request)
        return HttpResponseRedirect(reverse('blog_app:home'))
