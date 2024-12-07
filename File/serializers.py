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

    def create(self, validated_data):
        # Gắn tài khoản dựa trên user từ context
        try:
            account = AccountModel.objects.get(username=self.user.username)
        except AccountModel.DoesNotExist:
            account = None

        validated_data['account'] = account  # Gán tài khoản vào validated_data

        # Tạo instance mới
        return super().create(validated_data)
