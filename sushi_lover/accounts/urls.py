from django.urls import path

from sushi_lover.accounts.views import UserRegisterView, UserLoginView, UserLogoutView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='sign up'),
    path('login/', UserLoginView.as_view(), name='sign in'),
    path('logout/', UserLogoutView.as_view(), name='sign out'),
)

# Important
from sushi_lover.accounts.signals import *