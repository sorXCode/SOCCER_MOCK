from api.models import UserAccount, Staff, Team, Fixture
from api.serializers import (
    UserAccountSerializer, StaffSerializer, TeamSerializer, FixtureSerializer)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt import views as jwt_views
from django.http import HttpResponseRedirect, HttpResponse
import requests
from django.urls import reverse

class AccountSignup(APIView):
    # model = UserAccount

    def post(self, request, format=None, **kwargs):
        data = request.data
        serializer = UserAccountSerializer(
            data=data) if not kwargs['is_staff'] else StaffSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountLogin(jwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return super().post(request)

class FixturesList(APIView):
    model = Fixture

    def get(self, request, format=None):
        fixtures = self.model.objects.all()
        serializer = FixtureSerializer(fixtures, many=True)
        return Response(serializer.data)


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
