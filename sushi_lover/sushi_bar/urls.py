from django.urls import path

from sushi_lover.sushi_bar.views import CreateSushiBarView, EditSushiBarView, DeleteSushiBarView,\
    DeleteSushiBarDoneView, SushiBarListView, SushiBarUserListView,\
    SushiBarDetails, sushi_bar_like, sushi_bar_comment

urlpatterns = (
        path('create/', CreateSushiBarView.as_view(), name='sushi bar create'),
        path('edit/<int:pk>', EditSushiBarView.as_view(), name='sushi bar edit'),
        path('delete/<int:pk>', DeleteSushiBarView.as_view(), name='sushi bar delete'),
        path('delete-done/', DeleteSushiBarDoneView.as_view(), name='sushi bar delete done'),
        path('list/', SushiBarListView.as_view(), name='sushi bar list'),
        path('user-list/', SushiBarUserListView.as_view(), name='sushi bar user list'),
        path('details/<int:pk>', SushiBarDetails.as_view(), name='sushi bar details'),
        path('like/<int:pk>', sushi_bar_like, name='sushi bar like'),
        path('comment/<int:pk>', sushi_bar_comment, name='sushi bar comment'),
)