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
    serializer = TeamSerializer(objects, many=True)
    return Response(serializer.data)

def parse_object_update_request(request):
    required_fields = ['old_name', 'new_name', ]
    message = "This field is required"
    error_message = {field: [
        message, ] for field in required_fields if field not in request.data.keys()}
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


class TeamsList(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    """
    Creates, Retrieve, update or delete a team instance.
    """
    model = Team
    serializer_class = TeamSerializer

    def get_object(self, name):
        try:
            return self.model.objects.get(name=name)
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request):
        return get_serializer_data(model=self.model, serializer=self.serializer_class)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return post_serializer(serializer)

    def put(self, request, *args, **kwargs):
        try:
            old_name = request.data['old_name']
            new_name = request.data['new_name']
        except KeyError:
            return parse_object_update_request(request)
        return Response(model.update_team_name(old_name=old_name, new_name=new_name))



    def delete(self, request, *args, **kwargs):
        team_name = request.data['name']
        team = self.get_object(name=team_name)
        team.delete()
        return Response({"detail": f"{team_name} deleted"}, status=status.HTTP_202_ACCEPTED)



# class FixturesList(APIView):
#     model = Fixture
#     serializer_class = FixtureSerializer
#     def get(self, request, format=None):
#         return get_serializer_data(model=self.model, serializer=self.serializer_class)


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
