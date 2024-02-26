from django.contrib import admin
from django.urls import path, include

from shop.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('shop.urls', 'shop'), namespace='shop')),
    path('users/', include(('users.urls', 'users') , namespace='users')),
]
