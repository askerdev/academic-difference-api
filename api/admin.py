"""Admin panel settings"""

from django.contrib import admin

from .models import (
    AcademicDifference,
    AcademicGroup,
    Department,
    Student,
    Subject,
    Teacher,
)


class StudentInline(admin.TabularInline):
    model = Student


@admin.register(AcademicGroup)
class AcademicGroupAdmin(admin.ModelAdmin):
    """Admin panel for AcademicGroup model"""

    inlines = (StudentInline,)

    list_display = ("number",)
    search_fields = ("number",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin panel for Student model"""

    raw_id_fields = ("group",)

    list_display = ("user", "group__number", "telegram_id")
    autocomplete_fields = ("user", "group")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__username",
        "user__email",
        "group__number",
        "telegram_id",
    )
    list_filter = ("group__number",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin panel for Department model"""

    list_display = ("name",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin panel for Subject model"""

    list_display = ("name", "department")
    autocomplete_fields = ("department",)
    search_fields = ("name",)
    list_filter = ("department__name",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin panel for Teacher model"""

    list_display = ("user", "subject__name", "subject__department")
    filter_horizontal = ("subject",)
    autocomplete_fields = ("user",)
    list_filter = ("subject__name",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(AcademicDifference)
class AcademicDifferenceAdmin(admin.ModelAdmin):
    """Admin panel for AcademicDifference model"""

    list_display = (
        "student",
        "subject",
        "view_department",
        "deadline",
        "is_closed",
    )
    list_display_links = ("student",)
    list_filter = (
        "is_closed",
        "deadline",
        "subject__department__name",
    )
    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__user__username",
        "student__user__email",
        "student__group__number",
        "subject__name",
    )
    autocomplete_fields = ("student", "subject")
    list_editable = ("is_closed",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "deadline"

    @admin.display()
    def view_department(self, obj):
        return obj.subject.department

    view_department.short_description = "Department"
