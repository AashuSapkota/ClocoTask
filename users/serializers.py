from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'phone', 'dob', 'gender', 'address']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

        def create(self, validated_data):
            password = validated_data.pop('password')
            password_hash = make_password(password)
            user = User.objects.create_user(password=password, **validated_data)
            return user