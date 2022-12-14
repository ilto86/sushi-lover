from django.contrib.auth import views as auth_views, get_user_model, login
from django.views import generic as views
from django.urls import reverse_lazy

from sushi_lover.accounts.forms import UserCreateForm, UserLoginForm

UserModel = get_user_model()


class UserRegisterView(views.CreateView):
    template_name = "accounts/register.html"
    model = UserModel
    form_class = UserCreateForm
    success_url = reverse_lazy("homepage")

    # Signs the user in, after successful sign up
    def form_valid(self, form):
        user_sing_in = super().form_valid(form)
        login(self.request, self.object)
        return user_sing_in


class UserLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = UserLoginForm


class UserLogoutView(auth_views.LogoutView):
    pass
