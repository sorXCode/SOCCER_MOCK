from api.models import UserAccount, Staff, Team, Fixture
from api.serializers import (
    UserAccountSerializer, StaffSerializer, TeamSerializer, FixtureSerializer)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from rest_framework_simplejwt import views as jwt_views
# from django.http import HttpResponseRedirect, HttpResponse


def post_serializer(serializer):
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_serializer_data(model, serializer):
    objects = model.objects.all()
    serializer = serializer(objects, many=True)

    return Response(serializer.data)


def parse_object_update_request(request, required_fields):
    message = "This field is required"
    provided_fields = request.data.keys()
    error_message = {field: [message, ] for field in required_fields
                     if field not in provided_fields}
    if error_message:
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


class AccountSignup(APIView):
    # model = UserAccount

    def post(self, request, format=None, **kwargs):
        serializer = UserAccountSerializer(
            data=request.data) if not kwargs['is_staff'] else\
            StaffSerializer(data=request.data)

        return post_serializer(serializer)


class AccountLogin(jwt_views.TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        return super().post(request)


class TeamsAndFixturesMixin(APIView):

    def get_object(self, identifier=None):
        raise NotImplementedError

    def get(self, request, *args, **kwargs):
        return get_serializer_data(model=self.model, serializer=self.serializer_class)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return post_serializer(serializer)

    def put(self, request, *args, **kwargs):
        raise NotImplementedError

    def delete(self, request, *args, **kwargs):
        raise NotImplementedError

class TeamsList(TeamsAndFixturesMixin):
    """
    Creates, Retrieve, update or delete a team instance.
    """
    permission_classes = (IsAuthenticated, IsAdminUser)
    model = Team
    serializer_class = TeamSerializer

    def get_object(self, identifier):
        try:
            return self.model.objects.get(name=identifier)
        except self.model.DoesNotExist:
            raise Http404
    
    
    def put(self, request):
        try:
            old_name = request.data['old_name']
            new_name = request.data['new_name']
        except KeyError:
            return parse_object_update_request(request, required_fields=['old_name', 'new_name', ])
        return Response(self.model.update_team_name(old_name=old_name, new_name=new_name))
    
    def delete(self, request):
        object_name = request.data['name']
        team = self.get_object(identifier=object_name)
        team.delete()
        return Response({"detail": f"{object_name} deleted"}, status=status.HTTP_202_ACCEPTED)


class FixturesList(TeamsAndFixturesMixin):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    model = Fixture
    serializer_class = FixtureSerializer

    # implement unique for date for fixtures

    def get_object(self, identifier):
        try:
            return self.model.objects.get(link_address=identifier)
        except self.model.DoesNotExist:
            raise Http404

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                instance = self.get_object(identifier=kwargs['link_address'])
                serializer.update(instance=instance, validated_data=serializer.data)
                return Response(serializer.data)
            except KeyError:
                raise Http404
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object(identifier=kwargs['link_address'])
            instance.delete()
            return Response({"detail": f"{instance} deleted"}, status=status.HTTP_202_ACCEPTED)
        except KeyError:
            raise Http404

class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
