from django.contrib.auth.decorators import login_required as l
from django.urls import path
from apps.accounts.views import (AccountRegistrationView,
                                 AccountAuthenticationView,
                                 AccountLogoutView,
                                 AccountProfileEditView,
                                 AccountProfileView,
                                 AccountFollowers,
                                 AccountFollowings)

app_name = "accounts"

urlpatterns = [
    path('registration/', AccountRegistrationView.as_view(), name='registration'),
    path('login/', AccountAuthenticationView.as_view(), name='login'),
    path('logout/', l(AccountLogoutView.as_view(), redirect_field_name='login'), name='logout'),
    path('profile/user/<str:username>/', l(AccountProfileView.as_view()), name='profile'),
    path('profile/update/', l(AccountProfileEditView.as_view(), redirect_field_name='login'), name='profile-update'),
    path('profile/<str:username>/followers/', l(AccountFollowers.as_view(), redirect_field_name='login'),
         name='followers'),
    path('profile/<str:username>/followings/', l(AccountFollowings.as_view(), redirect_field_name='login'),
         name='followings'),
]
