from django import forms
from .models import FileModel
from Account.models import AccountModel
from django.core.exceptions import ValidationError

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file']
        labels = {
            'file': 'Chọn file của bạn:',
        }
        widgets = {
            'file': forms.ClearableFileInput(),
        }
    def save(self, commit=True, username=None):
        # Kiểm tra xem người dùng đã cung cấp tên người dùng chưa
        if username is None:
            raise ValidationError("Username không hợp lệ.")

        try:
            account = AccountModel.objects.get(username=username)
        except AccountModel.DoesNotExist:
            raise ValidationError(f"Không tìm thấy tài khoản với tên người dùng: {username}")

        # Lấy đối tượng FileModel và gán tài khoản vào
        file_instance = super().save(commit=False)
        file_instance.account = account

        if commit:
            file_instance.save()

        return file_instance
