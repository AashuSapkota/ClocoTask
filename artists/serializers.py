from rest_framework import serializers
from .models import Artists
from django.contrib.auth.hashers import make_password
from datetime import datetime


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = ['id','name', 'dob', 'gender', 'address', 'first_release_year', 'no_of_albums_released', 'created_at', 'updated_at']

    def create(self, validated_data):
        created_at = datetime.now()
        updated_at = datetime.now()
        artist = Artists.objects.create(created_at=created_at, updated_at='', **validated_data)
        return artist

    
