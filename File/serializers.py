from rest_framework import serializers
from .models import FileModel
from Account.models import AccountModel
from django.utils import timezone
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = "__all__"
        

class UploadFileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = FileModel
        fields = ['file', 'created_at', 'account']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lấy user từ context
        self.user = self.context.get('request').user

    def update(self, instance, validated_data):
        # Sử dụng self.user thay vì trực tiếp truy vấn request.user
        account = AccountModel.objects.get(username=self.user.username)
        instance.account = account
        instance.created_at = timezone.now()
        return super().update(instance, validated_data)