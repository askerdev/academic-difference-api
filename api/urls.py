"""Routes for api views"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
    path(
        "students/create/",
        views.create_student,
        name="create_student",
    ),
    path(
        "students/",
        views.list_students,
        name="list_students",
    ),
    path(
        "students/remove/",
        views.remove_student,
        name="remove_student",
    ),
    path(
        "students/<int:student_id>/",
        views.edit_student,
        name="edit_student",
    ),
]
