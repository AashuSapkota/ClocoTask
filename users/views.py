from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer
from rest_framework import status


class ListUsersAPI(APIView):
    pagination_class = PageNumberPagination
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginator.page_size = 2
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = self.serializer_class(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class RegisterUserAPI(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status': 'Success', 'Message': 'User Created Successfully'}, status=201)
        return Response({'Status': 'Error', 'Message': serializer.errors}, status=400)


class UpdateUserAPI(APIView):
    def put(self, request, user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': 'Error', 'Message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'Status': 'Error', 'Message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUserAPI(APIView):
    def delete(self, request, user_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'Status': 'Error', 'Message': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user = User.objects.get(pk=user_id)
            user.delete()

        except Exception as e:
            return Response({'Status': 'Error', 'Message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
