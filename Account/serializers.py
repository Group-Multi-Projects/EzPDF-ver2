from rest_framework import serializers
from .models import AccountModel
class AccountSerializer(serializers.Serializer):
    class Meta():
        model = AccountModel
        fields = "__all__"
        