"""Routes for api views"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import mvt
from api.views.rest import (
    AcademicDifferenceViewSet,
    AcademicGroupViewSet,
    DepartmentViewSet,
    StudentViewSet,
    SubjectViewSet,
    TeacherViewSet,
)

router = DefaultRouter()

router.register(r"students", StudentViewSet)
router.register(r"groups", AcademicGroupViewSet)
router.register(r"departments", DepartmentViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"teachers", TeacherViewSet)
router.register(r"academic-differences", AcademicDifferenceViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
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
