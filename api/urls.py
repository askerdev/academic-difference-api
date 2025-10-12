"""Routes for api views"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

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
]
