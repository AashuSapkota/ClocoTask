from rest_framework import serializers
from .models import Artists, Music
from django.contrib.auth.hashers import make_password
from datetime import datetime


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artists
        fields = ['id','name', 'dob', 'gender', 'address', 'first_release_year', 'no_of_albums_released', 'created_at', 'updated_at']

    def create(self, validated_data):
        created_at = datetime.now()
        updated_at = datetime.now()
        artist = Artists.objects.create(created_at=created_at, updated_at=updated_at, **validated_data)
        return artist

    

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'artist_id', 'title', 'album_name', 'genre', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)

        try:
            artist_id = Artists.objects.get(pk=ret['artist_id'])
            artist_name = artist_id.name
            ret['artist_name'] = artist_name
        except:
            ret['artist_name'] = ""
        
        return ret
    
    # def validate_artist_id(self, instance):
    #     ret = super().to_representation(instance)

    #     try:
    #         artist = Artists.objects.get(pk=ret['artist_id'])
    #     except Artists.DoesNotExist:
    #         raise serializers.ValidationError("Invalid artist_id")
        
    #     return ret
    def validate(self, attrs):
        artist_id = attrs.get('artist_id')
        if artist_id:
            try:
                artist = Artists.objects.get(pk=artist_id)
            except Artists.DoesNotExist:
                raise serializers.ValidationError({
                    'Status': 'Error',
                    'Message': 'Invalid artist_id'
                })
        return attrs

    
    def create(self, validated_data):
        created_at = datetime.now()
        updated_at = datetime.now()
        music = Music.objects.create(created_at=created_at, updated_at=updated_at, **validated_data)
        return music