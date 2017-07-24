"""wifidb URL Configuration
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from rest_framework import routers

from wifidb.settings import DEBUG

import accounts.urls

from devices.views import DeviceViewSet

router = routers.DefaultRouter()
router.register(r'device', DeviceViewSet, 'devices')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
    url(r'^accounts/', include(accounts.urls)),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^about[/]$', TemplateView.as_view(template_name="about.html")),
]

if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
