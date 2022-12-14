from django.urls import path

from sushi_lover.common.views import index

urlpatterns = (
    path('', index, name='homepage'),
)