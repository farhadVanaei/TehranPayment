from account.models import CustomUser as User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'phone_number']


class OTPRequestSerializer(serializers.Serializer):

    class Meta:
        pass
