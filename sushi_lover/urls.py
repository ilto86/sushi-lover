from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('sushi_lover.common.urls')),
    path('auth/', include('sushi_lover.accounts.urls')),
    path('profile/', include('sushi_lover.profiles.urls')),
    path('sushi/', include('sushi_lover.sushi.urls')),
    path('sushi-type/', include('sushi_lover.sushi_type.urls')),
    path('sushi-bar/', include('sushi_lover.sushi_bar.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)