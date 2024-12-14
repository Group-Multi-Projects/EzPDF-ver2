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
    request_type = serializers.CharField(default="Web", write_only=True)  # Chỉ ghi
    output_file_url = serializers.CharField(read_only = True)
    class Meta:
        model = FileModel
        fields = ['file', 'created_at', 'account','request_type','output_file_url']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Lấy user từ context
        self.user = self.context.get('request').user

    def create(self, validated_data):
        # Lấy các trường không phải thuộc tính của model
        request_type = validated_data.pop('request_type', None)

        # Gắn tài khoản dựa trên user từ context
        try:
            account = AccountModel.objects.get(username=self.user.username)
        except AccountModel.DoesNotExist:
            account = None

        validated_data['account'] = account  # Gán tài khoản vào validated_data

        # Tạo instance mới từ validated_data còn lại
        return super().create(validated_data)
