"""REST API Views"""

from datetime import date

from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django_filters import CharFilter, DateFromToRangeFilter, FilterSet
from django_filters.rest_framework import DjangoFilterBackend

from api.models import (
    AcademicDifference,
    AcademicGroup,
    Department,
    Student,
    Subject,
    Teacher,
)
from api.serializers import (
    AcademicDifferenceSerializer,
    AcademicGroupSerializer,
    DepartmentSerializer,
    StudentSerializer,
    SubjectSerializer,
    TeacherSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    """Student API View"""

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
    ]

    @action(methods=["GET"], detail=False)
    # pylint: disable=unused-argument
    def quiet(self, request):
        students = Student.objects.filter(settings__notifications=False)

        page = self.paginate_queryset(students)
        if page is not None:
            serializer = StudentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class AcademicGroupViewSet(viewsets.ModelViewSet):
    """AcademicGroup API View"""

    queryset = AcademicGroup.objects.all()
    serializer_class = AcademicGroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ["number"]


class DepartmentViewSet(viewsets.ModelViewSet):
    """Department API View"""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class SubjectViewSet(viewsets.ModelViewSet):
    """Subject API View"""

    queryset = Subject.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SubjectSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name"]

    @action(methods=["GET"], detail=False)
    def from_not_closed_for_user(self, request):

        subjects = Subject.objects.filter(
            (
                Q(teacher__user__username="maksimov")
                | Q(teacher__user__username="krasnikova")
            )
            & Q(academicdifference__student__user=request.user)
            & Q(academicdifference__is_closed=False)
        )

        page = self.paginate_queryset(subjects)
        if page is not None:
            serializer = SubjectSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    """Teacher API View"""

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [SearchFilter]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "subject__name",
    ]


class AcademicDifferenceFilterset(FilterSet):
    """AcademicDifference Filterset"""

    student_username = CharFilter(
        field_name="student__user__username",
        lookup_expr="icontains",
    )
    student_first_name = CharFilter(
        field_name="student__user__first_name",
        lookup_expr="icontains",
    )
    student_last_name = CharFilter(
        field_name="student__user__last_name",
        lookup_expr="icontains",
    )
    teacher_username = CharFilter(
        field_name="subject__teacher__user__username",
        lookup_expr="icontains",
    )
    teacher_first_name = CharFilter(
        field_name="subject__teacher__user__first_name",
        lookup_expr="icontains",
    )
    teacher_last_name = CharFilter(
        field_name="subject__teacher__user__last_name",
        lookup_expr="icontains",
    )
    subject = CharFilter(
        field_name="subject__name",
        lookup_expr="icontains",
    )
    deadline = DateFromToRangeFilter()

    class Meta:
        model = AcademicDifference
        fields = [
            "student_username",
            "student_first_name",
            "student_last_name",
            "teacher_username",
            "teacher_first_name",
            "teacher_last_name",
            "subject",
            "deadline",
        ]


class AcademicDifferenceViewSet(viewsets.ModelViewSet):
    """AcademicDifference API View"""

    queryset = AcademicDifference.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AcademicDifferenceSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "student__user__username",
        "student__user__first_name",
        "student__user__last_name",
        "subject__name",
    ]
    filterset_class = AcademicDifferenceFilterset

    def get_queryset(self):
        if self.request.user.is_superuser:
            return AcademicDifference.objects.all()
        return AcademicDifference.objects.filter(
            student__user=self.request.user
        )

    @action(methods=["GET"], detail=False)
    # pylint: disable=unused-argument
    def upcoming(self, request):
        today = date.today()

        differences = AcademicDifference.objects.filter(deadline__gte=today)

        page = self.paginate_queryset(differences)
        if page is not None:
            serializer = AcademicDifferenceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AcademicDifferenceSerializer(differences, many=True)
        return Response(serializer.data)

    @action(methods=["POST"], detail=True)
    # pylint: disable=unused-argument
    def close(self, request, pk=None):
        difference = self.get_object()
        difference.is_closed = True
        difference.save()
        serializer = AcademicDifferenceSerializer(difference)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def upcoming_for_teacher(self, request):
        differences = AcademicDifference.objects.filter(
            (
                Q(subject__teacher__user=request.user)
                if not request.user.is_superuser
                else Q()
            )
            & (
                Q(student__group__number="241-3210")
                | Q(student__group__number="241-322")
            )
            & Q(is_closed=False)
        )

        page = self.paginate_queryset(differences)
        if page is not None:
            serializer = AcademicDifferenceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AcademicDifferenceSerializer(differences, many=True)
        return Response(serializer.data)
