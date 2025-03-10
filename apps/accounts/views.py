from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.cache import cache

from apps.accounts.forms import AccountRegistrationForm, AccountAuthenticationForm, ProfileForm
from apps.accounts.models import Profile, CustomAccount, Follow
from apps.utils.db_queries import get_users_posts
from apps.utils.email_sender import SendEmail
from apps.utils.otp_generator import OTP_generator
from apps.utils.otp_verify_email_template import email_verify


class AccountRegistrationView(View):
    template_name = 'account/registration.html'

    def get(self, request):
        form = AccountRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = AccountRegistrationForm(request.POST)

        if form.is_valid():
            otp = OTP_generator(password_reset=False)
            cache.set(otp, form.data.get('email'), timeout=3600)
            status = SendEmail.send_email(subject="Your Account Has Been Created Get Verified",
                                          body=email_verify(otp=otp),
                                          to=[form.data.get("email")])
            if status is not False:
                form.save()
                return redirect('accounts:verify_email')

        else:
            return render(request, self.template_name, {'form': form})


class AccountAuthenticationView(View):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = AccountAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = AccountAuthenticationForm(data=request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)
                return redirect('news-feed')

        else:
            return render(request, self.template_name, {'form': form})


class AccountLogoutView(View):
    template_name = 'account/logout.html'

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return render(request, self.template_name)


class AccountProfileEditView(View):
    template_name = 'account/update_profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            profile_form = ProfileForm(instance=request.user.profile)
            return render(request, self.template_name, {'profile_form': profile_form})

    def post(self, request):
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('accounts:profile', username=request.user)
        else:
            print(profile_form.errors)
        return render(request, self.template_name, {'profile_form': profile_form})


class AccountProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(CustomAccount, username=username)
        posts = get_users_posts(user=user)
        is_following = Follow.objects.filter(follower=request.user, following=user).exists()
        followers_count = user.followers.count()
        following_count = user.following.count()

        context = {
            'user': user,
            'posts': posts,
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
        }
        return render(request, self.template_name, context)

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(CustomAccount, username=username)
        if user != request.user:
            follow_relation = Follow.objects.filter(follower=request.user, following=user)
            if follow_relation.exists():
                follow_relation.delete()
            else:
                Follow.objects.create(follower=request.user, following=user)
        return redirect('accounts:profile', username=username)


class AccountFollowers(View):
    template_name = 'account/followers.html'

    def get(self, request, username, *args, **kwargs):
        user = CustomAccount.objects.get(username=username)
        followers = user.followers.all()
        context = {
            'user': user,
            'followers': followers
        }
        return render(request, self.template_name, context)


class AccountFollowings(View):
    template_name = 'account/followings.html'

    def get(self, request, username, *args, **kwargs):
        user = CustomAccount.objects.get(username=username)
        followings = user.following.all()
        context = {
            'user': user,
            'followings': followings
        }
        return render(request, self.template_name, context)


class EmailVerificationView(View):
    template_name = 'account/otp_verification.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        cached_email = cache.get(otp)

        if cached_email == email:
            # Clear the cache after successful verification
            cache.delete(otp)
            messages.success(request, 'Email verified successfully. You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Invalid OTP or email. Please try again.')
            return render(request, self.template_name)
