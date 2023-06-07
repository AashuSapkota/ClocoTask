from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Artists
from .serializers import ArtistSerializer
import requests

# Create your views here.

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
        return Response({'Status': 'Error', 'Message': serializer.errors}, status=400)



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
        paginator.page_size = 2
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
                return Response({'Status': 'Error', 'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Artists.DoesNotExist:
            return Response({'Status': 'Error', 'Message': 'Artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class DeleteArtistAPI(APIView):
    permission_classes = [IsAuthenticated]
    # def get_permissions(self):
    #     if self.request.method == 'delete':
    #         return [IsAuthenticated()]
    #     return []

    def delete(self, request, artist_id, *args, **kwargs):
        try:
            artist = Artists.objects.get(pk=artist_id)
            artist.delete()
            return Response({'Status': 'Success', 'Message': 'Artist Deleted Successfully'}, status=200)

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)