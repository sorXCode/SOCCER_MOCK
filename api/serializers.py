from rest_framework import serializers
from api.models import UserAccount, Staff, Team, Fixture


def create_user(user_model, validated_data, is_staff=False, is_admin=False):
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
        user = create_user(user_model=self.Meta.model,
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
        user = create_user(user_model=self.Meta.model,
                           validated_data=validated_data,
                           is_staff=True,
                           is_admin=True)
        return user


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['name', ]


class FixtureSerializer(serializers.ModelSerializer):

    home_team = None
    away_team = None

    home_team = serializers.SlugRelatedField(
        slug_field="name", queryset=Team.objects.all())
    away_team = serializers.SlugRelatedField(
        slug_field="name", queryset=Team.objects.all())

    class Meta:
        model = Fixture
        exclude = ['fixed_at', 'id', ]

    def validate_home_team(self, *data):
        self.home_team = super().validate(data)[0]
        return self.home_team

    def validate_away_team(self, *data):
        self.away_team = super().validate(data)[0]
        return self.away_team

    def update(self, instance, validated_data):
        """
        Update and return an existing `fixture` instance, given the validated data.
        """

        validated_data['home_team'] = self.home_team
        validated_data['away_team'] = self.away_team
        
        return self.Meta.model.updateFixtureEvent(instance=instance, details=validated_data)
