import json
import os

from django.conf import settings
from django.contrib import admin

from devices.models import Category, Device, Signature
from devices.serializers import DeviceSerializer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    pass

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    filter_horizontal = ('signature_24','signature_5',)
    fields = ('uuid', 'name', 'thumbnail', 'category', 'mac_vendor', 'comment', 'created_at', 'modified_at', 'image', 'image_url','signature_24','signature_5', 'chipset')
    list_display = ('approved', 'thumbnail', 'name', 'mac_vendor', 'category', 'chipset', 'created_at', 'modified_at', 'comment')
    list_display_links = ('name',)
    list_filter = ('approved', 'category')
    search_fields = ('name', 'mac_vendor')
    readonly_fields = ('uuid', 'thumbnail', 'image_url',)
    actions = ['make_approved', 'export']

    def make_approved(self, request, queryset):
        rows_updated = queryset.update(approved=1)

        if rows_updated == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % rows_updated

        self.message_user(request, "%s successfully marked as approved." % message_bit)

    def export(self, request, queryset):
        n = 0

        for d in queryset:
            file_path = settings.JSON_DB_PATH + d.get_path()

            if not os.path.exists(file_path):
                os.makedirs(file_path)

            s = DeviceSerializer(d)
            with open(file_path + settings.JSON_DB_FILE_NAME, 'w') as f:
                s.data["image_url"] = s.data["image_url"].replace(settings.MEDIA_URL, '')
                f.write(json.dumps(s.data, indent=4))
                n += 1

        if n == 0:
            message_bit = "No device was"
        elif n == 1:
            message_bit = "1 device was"
        else:
            message_bit = "%s devices were" % n

        self.message_user(request, "%s successfully exported." % message_bit)

    export.short_description = "Export selected devices"
    make_approved.short_description = "Mark selected devices as approved"


admin.site.site_title = settings.ADMIN_NAME
admin.site.site_header = settings.ADMIN_NAME
