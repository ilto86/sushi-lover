from django.contrib.auth import mixins as auth_mixins, decorators as auth_decorators
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from sushi_lover.core.utilities import get_entity_by_pk
from sushi_lover.sushi_type.forms import SushiTypeCreateForm, SushiTypeEditForm, SushiTypeCommentForm
from sushi_lover.sushi_type.models import SushiType, SushiTypeLike


class CreateSushiTypeView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = SushiType
    template_name = 'sushi_type/sushi-type-create.html'
    form_class = SushiTypeCreateForm
    success_url = reverse_lazy('sushi type list')
    object = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class EditSushiTypeView(views.UpdateView):
    model = SushiType
    form_class = SushiTypeEditForm
    template_name = 'sushi_type/sushi-type-edit.html'

    def get_success_url(self):
        sushi_type_id = self.kwargs['pk']
        return reverse_lazy('sushi type details', kwargs={'pk': sushi_type_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiTypeView(views.DeleteView):
    model = SushiType
    template_name = 'sushi_type/sushi-type-delete.html'
    success_url = reverse_lazy('sushi type delete done')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiTypeDoneView(views.TemplateView):
    template_name = 'sushi_type/sushi-type-delete-done.html'


class SushiTypeListView(views.ListView):
    model = SushiType
    template_name = 'sushi_type/sushi-type-list.html'
    context_object_name = 'sushi_types'
    paginate_by = 3


class SushiTypeUserListView(views.ListView):
    model = SushiType
    template_name = 'sushi_type/sushi-type-user-list.html'
    context_object_name = 'sushi_types'
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()
        user = self.request.user
        return query_set.filter(user=user)


class SushiTypeDetails(views.DetailView):
    model = SushiType
    template_name = 'sushi_type/sushi-type-details.html'
    context_object_name = 'sushi_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sushi_type = context['sushi_type']
        sushi_type.likes_count = sushi_type.sushitypelike_set.count()
        sushi_type_comments = sushi_type.sushitypecomment_set.all()
        is_owner = sushi_type.user == self.request.user
        is_liked = sushi_type.sushitypelike_set.filter(user_id=self.request.user.id).exists()
        sushi_type_comment_form = SushiTypeCommentForm(
            initial={
                'object_pk': self.object.pk,
            }
        )

        context['sushi_type_comments'] = sushi_type_comments
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked
        context['sushi_type_comment_form'] = sushi_type_comment_form

        return context


@auth_decorators.login_required
def sushi_type_like(request, pk):
    sushi_type = get_entity_by_pk(SushiType, pk)
    like_by_user = sushi_type.sushitypelike_set.filter(user_id=request.user.id).first()

    if like_by_user:
        like_by_user.delete()
    else:
        like = SushiTypeLike(
            sushi_type=sushi_type,
            user=request.user,
        )
        like.save()

    return redirect('sushi type details', sushi_type.id)


@auth_decorators.login_required
def sushi_type_comment(request, pk):
    comment_form = SushiTypeCommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('sushi type details', pk)

