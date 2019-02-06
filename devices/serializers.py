from rest_framework import serializers

from devices.models import Category, Device, Signature


class CategorySerializer(serializers.ModelSerializer):

    parent = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    def get_parent(self, obj):
        if obj.parent is not None:
            return CategorySerializer(obj.parent).data
        else:
            return None

class SignatureSerializer(serializers.ModelSerializer):
    wifi_signature = serializers.CharField(max_length=255)

    class Meta:
        model = Signature
        fields = ('wifi_signature',)

class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.SerializerMethodField()
    category = serializers.IntegerField(write_only=True)
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    signature_24 = SignatureSerializer(read_only=True, many=True)
    signature_5 = SignatureSerializer(read_only=True, many=True)

    class Meta:
        model = Device
        fields = ('uuid', 'name', 'categories', 'category', 'mac_vendor', 'created_at', 'modified_at', 'image_url', 'signature_24', 'signature_5')

    def get_categories(self, obj):
        return obj.get_categories()

    def create(self, validated_data):
        cat = validated_data.get('category')
        uuid = validated_data.get('uuid')
        name = validated_data.get('name')
        category = Category.objects.get(id=cat)
        mac_vendor = validated_data.get('mac_vendor')
        created_at = validated_data.get('created_at')
        modified_at = validated_data.get('modified_at')
        image_url = validated_data.get('image_url')
        instance = Device.objects.create(uuid=uuid,
                        name=name,
                        category=category,
                        created_at=created_at,
                        mac_vendor=mac_vendor,
                        modified_at=modified_at,
                        image_url=image_url,
                        approved=True)
        instance = self.add_wifi_signatures(instance,validated_data)
        return instance

    def update(self, instance, validated_data):
        cat = validated_data.get('category')
        instance.name = validated_data.get('name', instance.name)
        instance.category = Category.objects.get(id=cat)
        instance.mac_vendor = validated_data.get('mac_vendor', instance.mac_vendor)
        instance.modified_at = validated_data.get('modified_at', instance.modified_at)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance = self.add_wifi_signatures(instance,validated_data)
        instance.save()
        return instance

    def add_wifi_signatures(self, instance, validated_data):
        if 'signature_24' in validated_data:
            sig_24 = validated_data.pop('signature_24')
            for sig_data in sig_24:
                try:
                    ex_sig = Signature.objects.get(wifi_signature=sig_data['wifi_signature'])
                except:
                    ex_sig = Signature.objects.create(**sig_data)
                instance.signature_24.add(ex_sig)

        if 'signature_5' in validated_data:
            sig_5 = validated_data.pop('signature_5')
            for sig_data in sig_5:
                try:
                    ex_sig = Signature.objects.get(wifi_signature=sig_data['wifi_signature'])
                except:
                    ex_sig = Signature.objects.create(**sig_data)
                instance.signature_5.add(ex_sig)
        return instance