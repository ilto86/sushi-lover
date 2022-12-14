from django.urls import path

from sushi_lover.profiles.views import ProfileDetailsView, ProfileEditView, ProfileDeleteView, ProfileDeleteDoneView

urlpatterns = (
    path('details/<int:pk>', ProfileDetailsView.as_view(), name='profile details'),
    path('edit/<int:pk>', ProfileEditView.as_view(), name='profile edit'),
    path('delete/<int:pk>', ProfileDeleteView.as_view(), name='profile delete'),
    path('delete-done/', ProfileDeleteDoneView.as_view(), name='profile delete done'),
)

# Important
from sushi_lover.profiles.signals import *