"""wifidb URL Configuration
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework import routers

from wifidb.settings import DEBUG

import accounts.urls

from devices.views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'device', DeviceViewSet, 'devices')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^accounts/', include(accounts.urls))
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
