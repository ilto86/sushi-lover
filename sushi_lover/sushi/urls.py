from django.urls import path

from sushi_lover.sushi.views import CreateSushiView, EditSushiView, DeleteSushiView, \
        DeleteSushiDoneView, SushiListView, SushiUserListView, \
        SushiDetails, sushi_like, sushi_comment

urlpatterns = (
        path('create/', CreateSushiView.as_view(), name='sushi create'),
        path('edit/<int:pk>', EditSushiView.as_view(), name='sushi edit'),
        path('delete/<int:pk>', DeleteSushiView.as_view(), name='sushi delete'),
        path('delete-done/', DeleteSushiDoneView.as_view(), name='sushi delete done'),
        path('list/', SushiListView.as_view(), name='sushi list'),
        path('user-list/', SushiUserListView.as_view(), name='sushi user list'),
        path('details/<int:pk>', SushiDetails.as_view(), name='sushi details'),
        path('like/<int:pk>', sushi_like, name='sushi like'),
        path('comment/<int:pk>', sushi_comment, name='sushi comment'),
)