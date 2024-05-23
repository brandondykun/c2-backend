"""
Views for the user api.
"""

from rest_framework import generics, permissions
from rest_framework.settings import api_settings
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from apps.core_app.models import Profile, User
from .serializers import (
    UserSerializer,
    ProfileDetailedSerializer,
    ProfileSerializer,
    UserProfileSerializer
)
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        if not username or not email or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # create User
        user_serializer = self.get_serializer(data={'email': email,
                                                    'password': password})
        user_serializer.is_valid(raise_exception=True)
        self.perform_create(user_serializer)
        # create Profile
        profile_serializer = ProfileSerializer(data={'username': username,
                                                     'user': user_serializer.data['id'],
                                                     'about': None})
        profile_serializer.is_valid(raise_exception=True)
        self.perform_create(profile_serializer)

        user = User.objects.get(id=user_serializer.data['id'])
        response_serializer = UserProfileSerializer(user)

        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user."""
        return self.request.user
    

@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='username', description='Username', type=str),
        ]
    )
)
class SearchCreateProfileView(generics.ListCreateAPIView):
    """Create a new Profile in the system or search for a profile by username."""
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    # TODO: permissions to search teams must be authenticated
    def get(self, request, *args, **kwargs):

        username = request.query_params.get('username', None)

        if not username:
            return Response({'message' : 'Must provide a username query param.'},
                            status=status.HTTP_400_BAD_REQUEST)
        

        profiles = Profile.objects.filter(username__icontains=username)
        serializer = self.serializer_class(profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveUpdateProfileView(generics.RetrieveUpdateAPIView):
    """Retrieve or update a Profile."""
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailedSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfileDetailedSerializer
        return ProfileSerializer


class RetrieveUserInfoView(generics.RetrieveAPIView):
    """Retrieve logged in user's profile."""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class SearchProfilesView(generics.ListAPIView):
#     """Search for a profile by username."""
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):

#         username = request.query_params.get('username', None)

#         if not username:
#             return Response({'message' : 'Must provide a username query param.'},
#                             status=status.HTTP_400_BAD_REQUEST)
        

#         profiles = Profile.objects.filter(username__icontains=username)
#         serializer = self.serializer_class(profiles, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)