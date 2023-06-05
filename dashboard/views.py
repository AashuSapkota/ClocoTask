from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class DashboardView(View):
    template_name = 'dashboard/base.html'
    context_object_name = 'user'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        return render(request, self.template_name, {'user':user})


