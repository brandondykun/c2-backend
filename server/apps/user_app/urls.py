"""
URL configuration for project_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'user_app'

urlpatterns = [
    path("create-user/", views.CreateUserView.as_view(), name="create_user"),
    path("users/<int:pk>/", views.RetrieveUpdateUserView.as_view(), name="retrieve_update_user"),
    path("profiles/", views.SearchCreateProfileView.as_view(), name="search_create_profile"),
    path("profiles/<int:pk>/", views.RetrieveUpdateProfileView.as_view(), name="retrieve_update_profile"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('my-info/', views.RetrieveUserInfoView.as_view(), name='my_info'),
]
