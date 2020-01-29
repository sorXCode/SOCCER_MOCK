from rest_framework import serializers
from api.models import UserAccount, Staff, Team, Fixture


def create(user_model, validated_data, is_staff=False):
    user = user_model.objects.create(
        username=validated_data['username'],
    )
    user.set_password(validated_data['password'])
    if is_staff:
        user.is_staff = True
    user.save()
    return user


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'password', 'token']
        write_only_fields = ('password',)
        extra_kwargs = {
            'id': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = create(user_model=self.Meta.model,
                      validated_data=validated_data)
        return user


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['username', 'email', 'password', 'token']
        write_only_fields = ('password',)
        read_only_fields = ('id', 'token', )
        extra_kwargs = {
            'id': {'write_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = create(user_model=self.Meta.model,
                      validated_data=validated_data,
                      is_staff=True)
        return user


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class FixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fixture
        fields = '__all__'
