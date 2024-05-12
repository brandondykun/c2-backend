from typing import Iterable
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile for each user."""
    username = models.CharField(max_length=32)
    about = models.CharField(max_length=1000)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE,
                            related_name='profile')
    
    def __str__(self):
        return self.username


class Team(models.Model):
    """Team that consists of members."""
    name = models.CharField(max_length=32)
    about = models.CharField(max_length=1000)
    created_at = models.DateTimeField()
    members = models.ManyToManyField(Profile,
                                     related_name="teams",
                                     blank=True)
    
    def save(self, *args, **kwargs):
        """On initial save, add created_at timestamp."""
        if not self.id:
            self.created_at = timezone.now()
        return super(Team, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Mission(models.Model):
    """Mission."""
    name = models.CharField(max_length=32)
    about = models.CharField(max_length=1000)
    teams = models.ManyToManyField(Team, related_name="missions", blank=True)
    created_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """On initial save, add created_at timestamp."""
        if not self.id:
            self.created_at = timezone.now()
        return super(Mission, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Point(models.Model):
    """Point."""
    class PointTypes(models.TextChoices):
        ENEMY = 'ENEMY', 'Enemy'
        FRIENDLY = 'FRIENDLY', 'Friendly'
        NEUTRAL = 'NEUTRAL', 'Neutral'
        UNKNOWN = 'UNKNOWN', 'Unknown'
        NAVIGATION = 'NAVIGATION', 'Navigation'

    type = models.CharField(
        max_length=12,
        choices=PointTypes.choices,
        default=PointTypes.NAVIGATION 
    )
    label = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    mgrs = models.CharField(max_length=20, null=True, blank=True)
    created_by = models.ForeignKey(Profile,
                                   on_delete=models.CASCADE,
                                   related_name='profile_points')
    created_at = models.DateTimeField(auto_now=True)
    mission = models.ForeignKey(Mission,
                                on_delete=models.CASCADE,
                                related_name='mission_points')
    team = models.ForeignKey(Team,
                             on_delete=models.CASCADE,
                             related_name='team_points')
        
    def __str__(self):
        return self.label
