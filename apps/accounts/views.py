from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from apps.accounts.forms import AccountRegistrationForm, AccountAuthenticationForm, ProfileForm
from apps.utils.db_queries import get_my_posts


class AccountRegistrationView(View):
    template_name = 'account/registration.html'

    def get(self, request):
        form = AccountRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        form = AccountRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:login')

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


class AccountProfileView(View):
    template_name = 'account/profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            my_posts = get_my_posts(request.user)
            return render(request, self.template_name,{'my_posts': my_posts})


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
            return redirect('accounts:profile')
        else:
            print(profile_form.errors)
        return render(request, self.template_name, {'profile_form': profile_form})
