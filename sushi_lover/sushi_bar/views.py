from django.core.exceptions import PermissionDenied
from folium import Map, Marker

from django.contrib.auth import mixins as auth_mixins, decorators as auth_decorators
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as views

from sushi_lover.core.utilities import get_entity_by_pk
from sushi_lover.sushi_bar.forms import SushiBarCreateForm, SushiBarEditForm, SushiBarCommentForm
from sushi_lover.sushi_bar.models import SushiBar, SushiBarLike


class CreateSushiBarView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = SushiBar
    template_name = 'sushi_bar/sushi-bar-create.html'
    form_class = SushiBarCreateForm
    success_url = reverse_lazy('sushi bar list')
    object = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)


class EditSushiBarView(views.UpdateView):
    model = SushiBar
    form_class = SushiBarEditForm
    template_name = 'sushi_bar/sushi-bar-edit.html'

    def get_success_url(self):
        sushi_bar_id = self.kwargs['pk']
        return reverse_lazy('sushi bar details', kwargs={'pk': sushi_bar_id})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiBarView(views.DeleteView):
    model = SushiBar
    template_name = 'sushi_bar/sushi-bar-delete.html'
    success_url = reverse_lazy('sushi bar delete done')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DeleteSushiBarDoneView(views.TemplateView):
    template_name = 'sushi_bar/sushi-bar-delete-done.html'


class SushiBarListView(views.ListView):
    model = SushiBar
    template_name = 'sushi_bar/sushi-bar-list.html'
    context_object_name = 'sushi_bars'
    paginate_by = 3


class SushiBarUserListView(views.ListView):
    model = SushiBar
    template_name = 'sushi_bar/sushi-bar-user-list.html'
    context_object_name = 'sushi_bars'
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()
        user = self.request.user
        return query_set.filter(user=user)


class SushiBarDetails(views.DetailView):
    model = SushiBar
    template_name = 'sushi_bar/sushi-bar-details.html'
    context_object_name = 'sushi_bar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sushi_bar = context['sushi_bar']
        sushi_bar_longitude = sushi_bar.longitude
        sushi_bar_latitude = sushi_bar.latitude
        location_map = None

        if sushi_bar_longitude and sushi_bar_latitude:
            location_map = Map(
                location=[
                    sushi_bar_latitude,
                    sushi_bar_longitude],
                zoom_start=20
            )

            Marker([
                sushi_bar_latitude,
                sushi_bar_longitude
            ],
                tooltip='Click',
                   popup=f'Sushi Bar name: {sushi_bar.name}'
                         f'\nSushi Bar address: {sushi_bar.address}'
                         f'\nLatitude: {sushi_bar_latitude}'
                         f'\nLongitude: {sushi_bar_longitude}'
            ).add_to(location_map)

            location_map = location_map._repr_html_()

        sushi_bar.likes_count = sushi_bar.sushibarlike_set.count()
        sushi_bar_comments = sushi_bar.sushibarcomment_set.all()
        is_owner = sushi_bar.user == self.request.user
        is_liked = sushi_bar.sushibarlike_set.filter(user_id=self.request.user.id).exists()
        sushi_bar_comment_form = SushiBarCommentForm(
            initial={
                'object_pk': self.object.pk,
            }
        )

        context['sushi_bar_location'] = location_map
        context['sushi_bar_comments'] = sushi_bar_comments
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked
        context['sushi_bar_comment_form'] = sushi_bar_comment_form

        return context


@auth_decorators.login_required
def sushi_bar_like(request, pk):
    sushi_bar = get_entity_by_pk(SushiBar, pk)
    like_by_user = sushi_bar.sushibarlike_set.filter(user_id=request.user.id).first()

    if like_by_user:
        like_by_user.delete()
    else:
        like = SushiBarLike(
            sushi_bar=sushi_bar,
            user=request.user,
        )
        like.save()

    return redirect('sushi bar details', sushi_bar.id)


@auth_decorators.login_required
def sushi_bar_comment(request, pk):
    comment_form = SushiBarCommentForm(request.POST)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('sushi bar details', pk)