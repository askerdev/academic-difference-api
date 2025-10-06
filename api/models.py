"""Academic difference models file"""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField

from simple_history.models import HistoricalRecords

User = get_user_model()


class Common(models.Model):
    """Common model for common fields"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)

    class Meta:
        """Common model Meta class."""

        abstract = True


class AcademicGroup(Common):
    """University Academic Group model"""

    number = models.CharField(
        max_length=255, unique=True, verbose_name="Academic Group Number"
    )

    class Meta:
        """Academic Group Meta class."""

        verbose_name = "academic group"
        verbose_name_plural = "academic groups"

    def __str__(self):
        return f"{self.number}"


class Student(Common):
    """University Student model"""

    user = models.OneToOneField(
        User, on_delete=models.PROTECT, verbose_name="Related user"
    )

    group = models.ForeignKey(
        AcademicGroup, on_delete=models.PROTECT, verbose_name="Related group"
    )

    telegram_id = models.BigIntegerField(
        unique=True, verbose_name="Telegram ID"
    )

    settings = JSONField(default=dict, blank=True, verbose_name="User Settings")

    class Meta:
        """Student Meta class."""

        verbose_name = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return (
            f"{self.user.last_name} {self.user.first_name} {self.group.number}"
        )


class Department(Common):
    """University Department model"""

    name = models.CharField(
        max_length=255, unique=True, verbose_name="Department Name"
    )

    class Meta:
        """Department Meta class."""

        verbose_name = "department"
        verbose_name_plural = "departments"

    def __str__(self):
        return self.name


class Subject(Common):
    """University Subject model"""

    name = models.CharField(
        max_length=255, unique=True, verbose_name="Subject Name"
    )

    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    class Meta:
        """Department Meta class."""

        verbose_name = "subject"
        verbose_name_plural = "subjects"

    def __str__(self):
        return self.name


class Teacher(Common):
    """University Teacher model"""

    user = models.OneToOneField(User, on_delete=models.PROTECT)

    subjects = models.ManyToManyField(
        Subject, verbose_name="Teacher To Subject"
    )

    class Meta:
        """Teacher Meta class."""

        verbose_name = "teacher"
        verbose_name_plural = "teachers"

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class AcademicDifference(Common):
    """Academic Difference model"""

    student = models.ForeignKey(Student, on_delete=models.PROTECT)

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    deadline = models.DateField()

    is_closed = models.BooleanField(default=False)

    class Meta:
        """Academic Difference Meta class."""

        verbose_name = "academic difference"
        verbose_name_plural = "academic differences"
