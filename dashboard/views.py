from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class DashboardView(APIView):
    template_name = 'dashboard/base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


