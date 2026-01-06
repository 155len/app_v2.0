from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.user.urls')),
    path('api/menu/', include('apps.menu.urls')),
    path('api/cart/', include('apps.cart.urls')),
    path('api/memos/', include('apps.memo.urls')),
    path('api/push/', include('apps.push.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
