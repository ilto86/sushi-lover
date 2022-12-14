from django.urls import path

from sushi_lover.sushi_type.views import CreateSushiTypeView, EditSushiTypeView, DeleteSushiTypeView,\
    DeleteSushiTypeDoneView, SushiTypeListView, SushiTypeUserListView,\
    SushiTypeDetails, sushi_type_like, sushi_type_comment

urlpatterns = (
        path('create/', CreateSushiTypeView.as_view(), name='sushi type create'),
        path('edit/<int:pk>', EditSushiTypeView.as_view(), name='sushi type edit'),
        path('delete/<int:pk>', DeleteSushiTypeView.as_view(), name='sushi type delete'),
        path('delete-done/', DeleteSushiTypeDoneView.as_view(), name='sushi type delete done'),
        path('list/', SushiTypeListView.as_view(), name='sushi type list'),
        path('user-list/', SushiTypeUserListView.as_view(), name='sushi type user list'),
        path('details/<int:pk>', SushiTypeDetails.as_view(), name='sushi type details'),
        path('like/<int:pk>', sushi_type_like, name='sushi type like'),
        path('comment/<int:pk>', sushi_type_comment, name='sushi type comment'),
)