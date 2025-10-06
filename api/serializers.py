"""Serializers for API"""

import json

from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import (
    AcademicDifference,
    AcademicGroup,
    Department,
    Student,
    Subject,
    Teacher,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class AcademicGroupSerializer(serializers.ModelSerializer):
    """AcademicGroup model serializer"""

    class Meta:
        model = AcademicGroup
        fields = ("number",)


class StudentSerializer(serializers.ModelSerializer):
    """Student model serializer"""

    user = UserSerializer()
    group = AcademicGroupSerializer()

    class Meta:
        model = Student
        fields = ("id", "user", "group", "telegram_id", "settings")

    def validate_settings(self, value):
        settings = json.loads(value)

        if "notifications" not in settings:
            raise serializers.ValidationError("notifications field is required")

        if settings["notifications"] not in (True, False):
            raise serializers.ValidationError(
                "notifications must be either True or False"
            )

        return value


class DepartmentSerializer(serializers.ModelSerializer):
    """Department model serializer"""

    class Meta:
        model = Department
        fields = ("id", "name")


class SubjectSerializer(serializers.ModelSerializer):
    """Subject model serializer"""

    class Meta:
        model = Subject
        fields = ("id", "name")


class TeacherSerializer(serializers.ModelSerializer):
    """Teacher model serializer"""

    user = UserSerializer()
    subjects = SubjectSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ("id", "user", "subjects")


class AcademicDifferenceSerializer(serializers.ModelSerializer):
    """AcademicDifference model serializer"""

    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = AcademicDifference
        fields = ("id", "student", "subject", "deadline", "is_closed")
