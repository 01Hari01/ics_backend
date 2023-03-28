from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Supplier


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'

    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Must include "username" and "password".')

        user = User.objects.filter(username=username).first()

        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        if not user.check_password(password):
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        data = super().validate(attrs)
        data['user'] = UserSerializer(user).data
        return data

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields='__all__'