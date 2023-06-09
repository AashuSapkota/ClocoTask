from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Artists, Music
from .serializers import ArtistSerializer, MusicSerializer
import requests
from rest_framework import serializers
from rest_framework.parsers import FileUploadParser
import csv
from django.http import HttpResponse
from rest_framework.settings import api_settings

# Create your views here.

class ArtistsUploadAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        try:
            file = request.data['file']
        except Exception as e:
            return Response({'Status':'Error', 'Message':'No file found.'}, status=400)
        
        artists_data = file.read().decode('utf-8')
        artists_list = list(csv.DictReader(artists_data.splitlines()))
        serializer = ArtistSerializer(data=artists_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artists Uploaded Successfully'}, status=201)
        return Response({'Status':'Error', 'Message':str(serializer.errors)}, status=400)


class ArtistsExportAPI(APIView):
    def get(self, request, *args, **kwargs):
        artists = Artists.objects.all()

        # create the CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="artists.csv"'

        # create a csv writer
        writer = csv.writer(response)

        # write the header row
        writer.writerow(['Name', 'DOB', 'Gender', 'Address', 'First Release Year', 'No of Albums'])

        # write artist data rows
        for artist in artists:
            writer.writerow([artist.name, artist.dob.date(), artist.gender, artist.address, artist.first_release_year, artist.no_of_albums_released])
        
        return response


class RegisterArtistAPI(APIView):
    template_name = 'artists/register_artist.html'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artist Added Successfully'}, status=201)
        return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=400)



class ListArtistsAPI(APIView):
    pagination_class = PageNumberPagination
    serializer_class = ArtistSerializer
    template_name = 'artists/list_artists.html'

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        artists = Artists.objects.all()
        paginator = self.pagination_class()
        page_size = api_settings.PAGE_SIZE
        paginator.page_size = page_size
        paginated_users = paginator.paginate_queryset(artists, request)
        serializer = self.serializer_class(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)
    


class UpdateArtistAPI(APIView):
    template_name='artists/update_artist.html'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    
    def get(self, request, *args, **kwargs):
        id = kwargs['artist_id']
        try:
            artist = Artists.objects.get(id=id)
            return render(request, self.template_name, {'artist':artist})
        except Exception as e:
            print(str(e))
    def put(self, request, *args, **kwargs):
        id = kwargs['artist_id']
        try:
            artist = Artists.objects.get(pk=id)
            serializer = ArtistSerializer(artist, data=request.data)
            if serializer.is_valid():
                print('valid')
                serializer.save()
                # return Response(serializer.data)
                return Response({'Status': 'Success', 'Message': 'Artist Updated Succesfully'}, status=200)
            else:
                return Response({'Status': 'Error', 'Message': str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Artists.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'Artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteArtistAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, artist_id, *args, **kwargs):
        try:
            artist = Artists.objects.get(pk=artist_id)
            artist.delete()
            return Response({'Status': 'Success', 'Message': 'Artist Deleted Successfully'}, status=200)

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FetchSimilarArtist(APIView):
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [IsAuthenticated()]
    #     return []
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        artist_name = request.GET.get('artist_name', '')
        similar_artists = Artists.objects.filter(name__icontains=artist_name).values_list('name', 'pk')
        print(similar_artists)
        return Response({'similar_artists':similar_artists})


class ListArtistMusicAPI(APIView):
    pagination_class = PageNumberPagination
    serializer_class = MusicSerializer
    template_name = 'artists/list_artists_music.html'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    
    def get(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        return render(request, self.template_name, {'artist_id':artist_id})
    
    def post(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        print(artist_id)
        musics = Music.objects.filter(artist_id=artist_id)
        print(musics)
        paginator = self.pagination_class()
        page_size = api_settings.PAGE_SIZE
        paginator.page_size = page_size
        paginated_users = paginator.paginate_queryset(musics, request)
        serializer = self.serializer_class(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class RegisterMusicAPI(APIView):
    template_name = 'artists/register_artist_music.html'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
        
    def get(self, request, *args, **kwargs):
        artist_id = kwargs["artist_id"]
        genre_choices = Music.GENRE_CHOICES
        return render(request, self.template_name, {'genre_choices': genre_choices, 'artist_id': artist_id})
    def post(self, request, *args, **kwargs):
        serializer = MusicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'Artist Added Successfully'}, status=201)
        except serializers.ValidationError as e:
            print(e)
            return Response({'Status': 'Error', 'Message': str(e.detail)}, status=400)


class DeleteArtistMusicAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        music_id = kwargs["music_id"]
        try:
            artist = Music.objects.get(pk=music_id)
            artist.delete()
            print("music deleted")
            return Response({'Status': 'Success', 'Message': 'Music Deleted Successfully'}, status=200)

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateArtistMusicAPI(APIView):
    template_name='artists/update_artists_music.html'
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return []
    
    def get(self, request, *args, **kwargs):
        print("GET")
        id = kwargs['music_id']
        genre_choices = Music.GENRE_CHOICES
        try:
            music = Music.objects.get(id=id)
            artist_id = music.artist_id
            artist = Artists.objects.get(id = artist_id)
            return render(request, self.template_name, {'music':music, 'artist':artist, 'genre_choices':genre_choices})
        except Exception as e:
            print(str(e))
    def put(self, request, *args, **kwargs):
        id = kwargs['music_id']
        try:
            artist = Music.objects.get(pk=id)
            serializer = MusicSerializer(artist, data=request.data)
            if serializer.is_valid():
                print('valid')
                serializer.save()
                # return Response(serializer.data)
                return Response({'Status': 'Success', 'Message': 'Music Updated Succesfully'}, status=200)
            else:
                return Response({'Status': 'Error', 'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Artists.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'Music does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)