from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from survival_kit import settings

from shop.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('users/', include(('users.urls', 'users'), namespace='users')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
