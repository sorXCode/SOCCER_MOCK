from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from uuid import uuid4
# Create your models here.


class GenerateTokenMixin:
    @property
    def token(self):
        return self._get_tokens()

    def _get_tokens(self):
        tokens = RefreshToken.for_user(self)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access
        }
        return data


class UserAccount(GenerateTokenMixin, User):

    class Meta:
        verbose_name = _("useraccount")
        verbose_name_plural = _("useraccounts")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("useraccount_detail", kwargs={"pk": self.pk})


class Staff(GenerateTokenMixin, User):

    class Meta:
        verbose_name = _("staffaccount")
        verbose_name_plural = _("staffaccounts")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("staffaccount_detail", kwargs={"pk": self.pk})


class Team(models.Model):

    def get_object(self, name):
            return self.model.objects.get(name=name)

    name = models.CharField(max_length=80, unique=True)

    class Meta:
        verbose_name = _("team")
        verbose_name_plural = _("teams")

    def __str__(self):
        return self.name
    
    @classmethod
    def update_team_name(cls, old_name, new_name):
        try:
            team = cls.objects.get(name=old_name)
            team.name = new_name
            team.save()
            return {"detail": f"{old_name} changed to {new_name}"}
        except cls.DoesNotExist:
            return {"detail": f"{old_name} does not exist"}
        except IntegrityError:
            return {"details": f"{new_name} already exist"}

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={"pk": self.pk})


class Fixture(models.Model):

    home_team = models.ForeignKey(
        Team, related_name='home_team', on_delete=models.CASCADE)
    away_team = models.ForeignKey(
        Team, related_name='away_team', on_delete=models.CASCADE)
    date_time = models.DateTimeField(blank=False)
    fixed_at = models.DateTimeField(auto_now=True)
    link_address = models.CharField(max_length=50, unique=True, default=uuid4)

    class Meta:
        verbose_name = _("fixture")
        verbose_name_plural = _("fixtures")
        ordering = ['date_time']

    @classmethod
    def updateFixtureEvent(cls, instance, details):
        instance.home_team = details['home_team']
        instance.away_team = details['away_team']
        instance.date_time = details['date_time']
        instance.save()
        
        return instance

    def __str__(self):
        return "{} vs {}".format(self.home_team, self.away_team)

    def get_absolute_url(self):
        return reverse("fixture_detail", kwargs={"pk": self.pk})
