from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, View
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
            user.profile_pic = request.FILES.get('profile_pic')
            user.about = request.POST.get('about')
            user.save()
            user.get_thumbnail()
            user.save()
            return HttpResponseRedirect(reverse('blog_app:login'))
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

        if not username or not password:
            error = "Please Input Username/Email and Password"
            return render(request, self.template_name, {'error': error})
        user = authenticate(request, username=username, password=password)
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


class ResetPassword(TemplateView):

    template_name = "blog_app/reset_passsword.html"

    def get(self, request, encoded=None):
        """get page"""
        decode = UTILS.decode(encoded)
        if decode.get('error'):
            error = "Link Expired"
            return render(request, self.template_name, {'fatal_error': error})
        user = User.objects.filter(id=decode.get('user_id'))
        if not user:
            error = "User Not Found Error."
            return render(request, self.template_name, {'fatal_error': error})
        user = user[0]
        return render(request, self.template_name, {'user': user.id})
    
    def post(self, request):
        """update password"""
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        user_id = request.POST.get('user_id')

        if not password or not confirm:
            error = "Please input new password"
            return render(request, self.template_name,
                          {'user': user_id,
                           'error': error})
        elif password != confirm:
            error = "Passwords do not match"
            return render(request, self.template_name,
                          {'user': user_id,
                           'error': error})
        user = User.objects.filter(id=user_id)
        if not user:
            error = "User Not Found Error."
            return render(request, self.template_name, {'fatal_error': error})
        user = user[0]
        if user.check_password(password):
            error = "New Password cannot be the same as Old Password. Input new password"
            return render(request, self.template_name,
                          {'error': error,
                           'user': user.id})
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse('blog_app:login'))


class ForgotPassword(TemplateView):

    template_name = 'blog_app/forgot_password.html'

    def get(self, request):
        """get page"""

        return render(request, self.template_name)
    
    def post(self, request):
        """send user password reset link"""

        email = request.POST.get('email')

        if not email:
            error = "Please input email"
            return render(request, self.template_name,
                          {'error': error})
        
        user = User.objects.filter(email=email)
        if not user:
            error = "User with email not found"
            return render(request, self.template_name,
                          {'error': error})
        user = user[0]
        UTILS.forgot_password(request, user.id, user.email)
        success = "Check Your Email For Reset Link"
        return render(request, self.template_name, {'success': success})


class UserDetailView(DetailView):

    model = User
    template_name = "blog_app/profile.html"
    context_object_name = 'user_profile'



class UserEditView(TemplateView):

    template_name = 'blog_app/edit_profile.html'

    def get(self, request):
        """get page for user edit"""

        if request.user.is_authenticated:
            return render(request, self.template_name)
        return HttpResponseRedirect(reverse('blog_app:home'))
    
    def post(self, request):
        """update user data"""

        if request.user.is_authenticated:
            print(request.POST.get('password'), request.POST.get('confirm_password'))
            user = request.user
            changeable = ['first_name', 'last_name', 'about']
            if 'password' in request.POST:
                user.set_password(request.POST.get('password'))
            for i in request.POST:
                if i in changeable and request.POST.get(i) != '':
                    setattr(user, i, request.POST.get(i))
            user.save()
            if request.FILES.get('profile_pic'):
                user.profile_pic = request.FILES.get('profile_pic')
                user.save()
                user.get_thumbnail()
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('blog_app:user_detail', args=[user.id]))
        return HttpResponseRedirect(reverse('blog_app:home'))

