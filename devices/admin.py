from django.conf import settings
from django.contrib import admin

from devices.models import Category, Device
from devices.forms import DeviceForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    form = DeviceForm
    fields = ('uuid', 'name', 'thumbnail', 'category', 'wifi_signature', 'mac_vendor', 'comment', 'created_at', 'modified_at', 'image', 'image_url')
    list_display = ('approved', 'thumbnail', 'name', 'mac_vendor', 'category', 'created_at', 'modified_at', 'comment')
    list_display_links = ('name',)
    list_filter = ('approved', 'category')
    search_fields = ('name', 'mac_vendor')
    readonly_fields = ('uuid', 'thumbnail', 'image_url',)
    actions = ['make_approved']

    def make_approved(self, request, queryset):
        rows_updated = queryset.update(approved=1)

        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated

        self.message_user(request, "%s successfully marked as approved." % message_bit)

    make_approved.short_description = "Mark selected devices as approved"


admin.site.site_title = settings.ADMIN_NAME
admin.site.site_header = settings.ADMIN_NAME
