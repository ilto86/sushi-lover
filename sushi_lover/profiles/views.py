from django.contrib.auth import get_user_model, logout
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from sushi_lover.profiles.forms import AppProfileForm
from sushi_lover.profiles.models import AppProfile

UserModel = get_user_model()


class ProfileDetailsView(views.DetailView):
    model = AppProfile
    template_name = 'profiles/profile-details.html'
    context_object_name = 'profile'


class ProfileEditView(views.UpdateView):
    model = AppProfile
    form_class = AppProfileForm
    template_name = 'profiles/profile-edit.html'

    def get_success_url(self):
        app_profile_id = self.kwargs['pk']
        return reverse_lazy('profile details', kwargs={'pk': app_profile_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfileDeleteView(views.DeleteView):
    model = UserModel
    template_name = 'profiles/profile-delete.html'

    def get_success_url(self):
        logout(self.request)
        return reverse('profile delete done')


class ProfileDeleteDoneView(views.TemplateView):
    template_name = 'profiles/profile-delete-done.html'
