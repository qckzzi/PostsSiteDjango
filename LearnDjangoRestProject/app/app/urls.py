from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from exchange_app.views import page_not_found
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exchange_app.urls')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
