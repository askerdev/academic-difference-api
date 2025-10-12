"""
Main URL Configuration
The `urlpatterns` list routes URLs.
"""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import mvt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path(
        "api/v1/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # model view template
    path(
        "students/create/",
        mvt.create_student,
        name="create_student",
    ),
    path(
        "students/",
        mvt.list_students,
        name="list_students",
    ),
    path(
        "students/remove/",
        mvt.remove_student,
        name="remove_student",
    ),
    path(
        "students/<int:student_id>/",
        mvt.edit_student,
        name="edit_student",
    ),
]
