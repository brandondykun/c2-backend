"""
Views for the mission api.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics, permissions
from apps.core_app.models import Profile
from apps.user_app.serializers import ProfileSerializer
from apps.core_app.models import Team, Mission, User, Point
from .serializers import (
    TeamSerializer,
    TeamDetailedSerializer,
    TeamMemberSerializer,
    MissionSerializer,
    MissionDetailedSerializer,
    MissionTeamSerializer,
    PointSerializer,
    PointDetailedSerializer,
    MissionGraphicsSerializer
)
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter
)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='teamName', description='Team Name', type=str),
        ]
    )
)
class ListCreateTeamView(generics.ListCreateAPIView):
    """Create a new Team in the system."""
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def create(self, request, *args, **kwargs):
        ## TODO: add error handling here
        new_team = Team.objects.create(**request.data)
        new_team.members.add(self.request.user.profile)
        new_team.save()
        serializer = TeamDetailedSerializer(new_team)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        team_name = request.query_params.get('teamName', None)
        if team_name:
            teams = Team.objects.filter(name__icontains=team_name)
            serializer = self.serializer_class(teams, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        teams = Team.objects.filter(members=request.user.profile).order_by('-created_at')
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateTeamView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a Profile."""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET', 'PATCH']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamDetailedSerializer
        return TeamSerializer


class AddMemberToTeamView(generics.UpdateAPIView):
    """Add a member to a team."""
    queryset = Team.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PATCH']

    def patch(self, request, *args, **kwargs):
        id = self.request.data['id']
        instance = self.get_object()
        instance.members.add(id)
        updated_members = instance.members.all()
        serializer = ProfileSerializer(updated_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveMemberFromTeamView(generics.DestroyAPIView):
    """Remove a member from a team."""
    queryset = Team.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        profile_id = kwargs['profile_id']
        instance = self.get_object()
        instance.members.remove(profile_id)
        updated_members = instance.members.all()
        serializer = ProfileSerializer(updated_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Mission Views

class ListCreateMissionView(generics.ListCreateAPIView):
    """List or create a new Mission in the system."""
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]
 
    def get_queryset(self):
        profile = Profile.objects.get(user=self.request.user)
        queryset = Mission.objects.filter(teams__members__id=profile.id).distinct()
        return queryset
    
    def create(self, request, *args, **kwargs):
        team_id = request.data.pop('teamId', None)

        if team_id:
        ## TODO: add error handling here
            new_mission = Mission.objects.create(**request.data)
            new_mission.teams.add(team_id)
            new_mission.save()
            serializer = MissionDetailedSerializer(new_mission)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response({ 'message': 'Please provide a team id.'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MissionDetailedSerializer
        return MissionSerializer
    

class RetrieveUpdateMissionView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a Mission."""
    queryset = Mission.objects.all()
    serializer_class = Mission
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET', 'PATCH']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MissionDetailedSerializer
        return MissionSerializer
    

class AddTeamToMissionView(generics.UpdateAPIView):
    """Add a Team to a Mission."""
    queryset = Mission.objects.all()
    serializer_class = MissionTeamSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PATCH']

    def patch(self, request, *args, **kwargs):
        id = request.data['teamId']
        instance = self.get_object()
        instance.teams.add(id)
        updated_teams = instance.teams.all()
        serializer = TeamDetailedSerializer(updated_teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveTeamFromMissionView(generics.DestroyAPIView):
    """Remove a team from a mission."""
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        team_id = kwargs['team_id']
        instance = self.get_object()
        instance.teams.remove(team_id)
        updated_members = instance.teams.all()
        serializer = TeamSerializer(updated_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class RetrieveMissionGraphicsView(generics.RetrieveAPIView):
    """Retrieve graphics for a Mission."""
    queryset = Mission.objects.all()
    serializer_class = MissionGraphicsSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET']
    

# Points Views

@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='mission', description='Mission ID', type=int, required=False),
            OpenApiParameter(name='team', description='Team ID', type=int, required=False),
        ]
    )
)
class ListCreatePointsView(generics.ListCreateAPIView):
    """List or create a new Point in the system."""
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        mission = request.query_params.get('mission', None)
        team = request.query_params.get('team', None)
        # TODO: Check if request profile is member of mission
        if mission:
            points = Point.objects.filter(mission=mission)
            serializer = self.serializer_class(points, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if team:
            points = Point.objects.filter(team=team)
            serializer = self.serializer_class(points, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Must provide team or mission query param'},
                        status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        newPointData = {
            **request.data,
            'created_by': request.user.profile.id
        }
        serializer = self.serializer_class(data=newPointData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdatePointView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a Point."""
    queryset = Point.objects.all()
    serializer_class = PointSerializer
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['GET', 'PATCH']
