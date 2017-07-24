from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.exceptions import NotFound

from devices.models import Category, Device
from devices.serializers import CategorySerializer, DeviceSerializer

try:
    from wifidb.settings import OUI_FILE
    from utils import manuf
except ImportError:
    OUI_FILE = False


def get_category_children_ids(cat, cat_ids):
    cat_ids.append(cat.id)

    if cat.child:
        for child in cat.child.all():
            cat_ids = get_category_children_ids(child, cat_ids)

    return cat_ids


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DeviceViewSet(viewsets.ModelViewSet):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        queryset = Device.objects.all().filter(approved=True)
        id = self.request.query_params.get('id', None)
        category = self.request.query_params.get('category', None)
        signature = self.request.query_params.get('signature', None)
        oui = self.request.query_params.get('oui', None)

        if id is not None:
            queryset = queryset.filter(id=id)
        elif category is not None:
            parent = get_object_or_404(Category.objects, name=category)
            cat_ids = []
            cat_ids = get_category_children_ids(parent, cat_ids)
            queryset = queryset.filter(category__id__in=cat_ids)
        elif signature is not None:
            queryset = queryset.filter(wifi_signature=signature)

            if OUI_FILE:
                if oui is not None:
                    oui_vendor_name = manuf.get_oui_vendor_name(oui, OUI_FILE)

                    if oui_vendor_name:
                        queryset = queryset.filter(mac_vendor=oui_vendor_name)
                    else:
                        raise NotFound(detail="OUI not found in database.", code=404)

        return queryset
