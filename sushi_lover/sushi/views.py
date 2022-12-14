from django.contrib.auth import decorators as auth_decorators, mixins as auth_mixins
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views


from sushi_lover.core.utilities import get_entity_by_pk
from sushi_lover.sushi.forms import SushiCreateForm, SushiEditForm, SushiCommentForm
from sushi_lover.sushi.models import Sushi, SushiLike
from sushi_lover.sushi_type.models import SushiType


class CreateSushiView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Sushi
    template_name = 'sushi/sushi-create.html'
    form_class = SushiCreateForm
    success_url = reverse_lazy('sushi list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['type'].queryset = SushiType.objects.filter(user=self.request.user)
        return form


class EditSushiView(views.UpdateView):
    model = Sushi
    form_class = SushiEditForm
    template_name = 'sushi/sushi-edit.html'

    def get_success_url(self):
        sushi_id = self.kwargs['pk']
        return reverse_lazy('sushi details', kwargs={'pk': sushi_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiView(views.DeleteView):
    model = Sushi
    template_name = 'sushi/sushi-delete.html'
    success_url = reverse_lazy('sushi delete done')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiDoneView(views.TemplateView):
    template_name = 'sushi/sushi-delete-done.html'


class SushiListView(views.ListView):
    model = Sushi
    template_name = 'sushi/sushi-list.html'
    context_object_name = 'sushi_all'
    paginate_by = 3


class SushiUserListView(views.ListView):
    model = Sushi
    template_name = 'sushi/sushi-user-list.html'
    context_object_name = 'sushi_all'
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()
        user = self.request.user
        return query_set.filter(user=user)


class SushiDetails(views.DetailView):
    model = Sushi
    template_name = 'sushi/sushi-details.html'
    context_object_name = 'sushi'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sushi = context['sushi']
        sushi.likes_count = sushi.sushilike_set.count()
        sushi_comments = sushi.sushicomment_set.all()
        is_owner = sushi.user == self.request.user
        is_liked = sushi.sushilike_set.filter(user_id=self.request.user.id).exists()
        sushi_comment_form = SushiCommentForm(
            initial={
                'object_pk': self.object.pk,
            }
        )

        context['sushi_comments'] = sushi_comments
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked
        context['sushi_comment_form'] = sushi_comment_form

        return context


@auth_decorators.login_required
def sushi_like(request, pk):
    sushi = get_entity_by_pk(Sushi, pk)
    like_by_user = sushi.sushilike_set.filter(user_id=request.user.id).first()

    if like_by_user:
        like_by_user.delete()
    else:
        like = SushiLike(
            sushi=sushi,
            user=request.user,
        )
        like.save()

    return redirect('sushi details', sushi.id)


@auth_decorators.login_required
def sushi_comment(request, pk):
    comment_form = SushiCommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('sushi details', pk)


