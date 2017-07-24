from uuid import UUID

from rest_framework import serializers
from devices.models import Category, Device


class CategorySerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_parent(self, obj):
        if obj.parent is not None:
            return CategorySerializer(obj.parent).data
        else:
            return None


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    # categories = serializers.SerializerMethodField()
    categories = CategorySerializer(read_only=True)
    category = serializers.IntegerField(write_only=True)
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    class Meta:
        model = Device
        fields = ('uuid', 'name', 'categories', 'category', 'wifi_signature', 'mac_vendor', 'created_at', 'modified_at', 'image_url')

    # def get_categories(self, obj):
    #     return obj.get_categories()

    def create(self, validated_data):
        cat = validated_data.get('category')
        uuid = validated_data.get('uuid')
        name = validated_data.get('name')
        category = Category.objects.get(id=cat)
        wifi_signature = validated_data.get('wifi_signature')
        mac_vendor = validated_data.get('mac_vendor')
        created_at = validated_data.get('created_at')
        modified_at = validated_data.get('modified_at')
        image_url = validated_data.get('image_url')
        return Device.objects.create(uuid=uuid,
                                     name=name,
                                     wifi_signature=wifi_signature,
                                     category=category,
                                     created_at=created_at,
                                     mac_vendor=mac_vendor,
                                     modified_at=modified_at,
                                     image_url=image_url)

    def update(self, instance, validated_data):
        cat = validated_data.get('category')
        instance.name = validated_data.get('name', instance.name)
        instance.category = Category.objects.get(id=cat)
        instance.wifi_signature = validated_data.get('wifi_signature', instance.wifi_signature)
        instance.mac_vendor = validated_data.get('mac_vendor', instance.mac_vendor)
        instance.modified_at = validated_data.get('modified_at', instance.modified_at)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.save()
        return instance
