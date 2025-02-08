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
    output_file_url = serializers.CharField(read_only=True)

    class Meta:
        model = FileModel
        fields = ['file', 'created_at', 'account', 'request_type', 'output_file_url']
        extra_kwargs = {'account': {'read_only': True}}  # Ngăn chặn người dùng gửi giá trị này

