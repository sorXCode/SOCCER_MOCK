from rest_framework import serializers
from api.models import UserAccount, Staff, Team, Fixture


def create(user_model, validated_data, is_staff=False, is_admin=False):
    user = user_model.objects.create(
        username=validated_data['username'],
    )
    user.set_password(validated_data['password'])
    if is_staff:
        user.is_staff = True
    if is_admin:
        user.is_admin = True
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
                      is_staff=True,
                      is_admin=True)
        return user


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', ]

    def create(self, validated_data):
        """
        Creates and return a new `Team` instance, given the validated data.
        """
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Team` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class FixtureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fixture
        fields = '__all__'

    def create(self, **validated_data):
        """
        Creates and return a new `Team` instance, given the validated data.
        """
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, **validated_data):
        """
        Update and return an existing `Team` instance, given the validated data.
        """
        instance.home_team = validated_data.get('home_team', instance.home_tem)
        instance.away_team = validated_data.get(
            'away_team', instance.away_team)
        instance.date_time = validated_data.get(
            'date_time', instance.date_time)
        instance.save()
        return instance
