"""
Tests for the teams api.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from apps.core_app.models import Profile, Team

MY_INFO_URL = reverse('user_app:my_info')
LOGIN_URL = reverse('user_app:token_obtain_pair')
REFRESH_TOKEN_URL = reverse('user_app:token_refresh')
CREATE_USER_URL = reverse('user_app:create_user')



def create_team(**params):
    """Create and return new Team."""
    return Team.objects.create_user(**params)


def create_user(**params):
    """Create and return new User."""
    return get_user_model().objects.create_user(**params)


def create_profile(**params):
    """Create and return new Profile."""
    return Profile.objects.create(**params)


LIST_CREATE_TEAM_URL = reverse('mission_app:create_team')
# RETRIEVE_UPDATE_TEAM_URL = reverse('mission_app:retrieve_update_team')
# ADD_MEMBER_TO_TEAM_URL = reverse('mission_app:add_member_to_team')
# REMOVE_MEMBER_FROM_TEAM_URL = reverse('mission_app:remove_member_from_team')

def retrieve_update_team_url(pk):
    """Create and return retrieve update team url."""
    return reverse('mission_app:retrieve_update_team', args=[pk])

def add_member_to_team_url(pk):
    """Create and return add member to team url."""
    return reverse('mission_app:add_member_to_team', args=[pk])

def remove_member_from_team_url(pk, profile_id):
    """Create and return remove member from team url."""
    return reverse('mission_app:remove_member_from_team', args=[pk, profile_id])


class CreateTeamApiTests(TestCase):
    """Test the private features of the Team API."""

    def setUp(self):
        user_details = {
            'email': 'test@example.com',
            'password': 'test-user-password-123'
        }
        self.user = create_user(**user_details)
        profile_details = {
            'username': 'test_username',
            'about': 'Test user about text.',
            'user': self.user
        }
        self.profile = create_profile(**profile_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_team(self):
        """Test creating a Team."""
        new_team = {
            "name": "Test Team",
            "about": "Test team about.",
        }
        res = self.client.post(LIST_CREATE_TEAM_URL, data=new_team)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
