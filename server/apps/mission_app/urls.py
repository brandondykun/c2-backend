from django.urls import path
from . import views

urlpatterns = [
    # TEAM URLS
    path("teams/", views.ListCreateTeamView.as_view(),
         name="create_team"),
    path("teams/<int:pk>/", views.RetrieveUpdateTeamView.as_view(),
         name="retrieve_update_team"),
    path("teams/<int:pk>/add-member/", views.AddMemberToTeamView.as_view(),
         name="add_member_to_team"),
    path("teams/<int:pk>/remove-member/<int:profile_id>/",
         views.RemoveMemberFromTeamView.as_view(),
         name="remove_member_from_team"),
    # MISSION URLS
    path("missions/", views.ListCreateMissionView.as_view(),
         name="list_create_mission"),
    path("missions/<int:pk>/", views.RetrieveUpdateMissionView.as_view(),
         name="retrieve_update_mission"),
    path("missions/<int:pk>/add-team/", views.AddTeamToMissionView.as_view(),
         name="add_team_to_mission"),
    path("missions/<int:pk>/graphics/", views.RetrieveMissionGraphicsView.as_view(),
         name="retrieve_mission_graphics"),
    path("missions/<int:pk>/remove-team/<int:team_id>/",
         views.RemoveTeamFromMissionView.as_view(),
         name="remove_team_from_mission"),
    # POINTS URLS
    path("points/", views.ListCreatePointsView.as_view(),
         name="list_create_point"),
    path("points/<int:pk>/", views.RetrieveUpdatePointView.as_view(),
         name="retrieve_update_point"),         
]
