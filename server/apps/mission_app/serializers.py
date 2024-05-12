"""
Serializers for the mission API view.
"""

from apps.user_app.serializers import ProfileSerializer
from rest_framework import serializers
from apps.core_app.models import Team, Profile, Mission, Point


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Teams."""
    class Meta:
        model = Team
        fields = ['id', 'name', 'about', 'created_at', 'members']
        read_only_fields = ['created_at', 'members']


class TeamDetailedSerializer(serializers.ModelSerializer):
    """Detailed serializer for Teams."""
    members = ProfileSerializer(many=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'about', 'created_at', 'members']


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer to add a member to a team."""
    id = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ['id']


class MissionSerializer(serializers.ModelSerializer):
    """Serializer for Missions."""

    class Meta:
        model = Mission
        fields = ['id', 'name', 'about', 'teams', 'created_at']


class MissionDetailedSerializer(serializers.ModelSerializer):
    """Serializer for Missions."""
    teams = TeamSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'name', 'about', 'teams', 'created_at']

        


class MissionTeamSerializer(serializers.ModelSerializer):
    """Serializer to add a team to a mission."""
    id = serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ['id']


class PointSerializer(serializers.ModelSerializer):
    """Serializer for Points."""
    class Meta:
        model = Point
        fields = ['id', 'type', 'label', 'description', 
                  'lat', 'lng', 'created_by', 'created_at', 
                  'mission', 'team', 'mgrs']
        read_only_fields = ['created_at']


class PointDetailedSerializer(serializers.ModelSerializer):
    """Detailed Serializer for Points."""
    created_by = ProfileSerializer()
    mission = MissionSerializer()
    team = TeamSerializer()

    class Meta:
        model = Point
        fields = ['id', 'type', 'label', 'description', 
                  'lat', 'lng', 'created_by', 'created_at', 
                  'mission', 'team', 'mgrs']
        read_only_fields = ['created_by', 'created_at']


class MissionGraphicsSerializer(serializers.ModelSerializer):
    """Mission Graphics Serializer."""
    mission_points = PointSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'name', 'mission_points']
