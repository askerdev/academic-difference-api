"""MVT API Views"""

import json

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from api.forms import CreateStudentForm, EditStudentForm
from api.models import AcademicGroup, Student

User = get_user_model()


@login_required()
def list_students(request):
    """List all students in database"""
    students = Student.objects.all()
    return render(request, "students/index.html", {"students": students})


@login_required()
def remove_student(request):
    """Remove student from database"""
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    with transaction.atomic():
        student = get_object_or_404(Student, pk=request.POST["student_id"])
        user = student.user
        student.delete()
        user.delete()

    return HttpResponseRedirect("/students/")


@login_required()
def create_student(request):
    """Create a new student"""
    if request.method == "POST":
        form = CreateStudentForm(request.POST)

        if not request.user.is_superuser:
            form.add_error(None, "only superusers can create students")
            return render(request, "students/create.html", {"form": form})

        if form.is_valid():
            try:
                with transaction.atomic():
                    user = User.objects.create(
                        username=form.cleaned_data["username"],
                        first_name=form.cleaned_data["first_name"],
                        last_name=form.cleaned_data["last_name"],
                        password=form.cleaned_data["password"],
                    )

                    student = Student.objects.create(
                        user=user,
                        telegram_id=form.cleaned_data["telegram_id"],
                        settings=form.cleaned_data["settings"],
                        group=AcademicGroup.objects.get(
                            number=form.cleaned_data["group"]
                        ),
                    )

                    user.save()
                    student.save()
                return HttpResponseRedirect(f"/students/{student.id}/")
            except AcademicGroup.DoesNotExist:
                form.add_error("group", "group does not exist")
                return render(request, "students/create.html", {"form": form})
            except IntegrityError as e:
                form.add_error(None, e.args[0])
                return render(request, "students/create.html", {"form": form})
    return render(
        request, "students/create.html", {"form": CreateStudentForm()}
    )


@login_required()
def edit_student(request, student_id):
    """Retrieve details of a single student"""
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        if request.user.id != student.user.id and not request.user.is_superuser:
            form = EditStudentForm(request.POST)
            form.add_error(None, "you can edit only yourself")
            return render(request, "students/detail.html", {"form": form})

        form = EditStudentForm(request.POST)
        if form.is_valid():
            try:
                student.group = AcademicGroup.objects.get(
                    number=form.cleaned_data["group"]
                )
            except AcademicGroup.DoesNotExist:
                form.add_error("group", "group does not exist")
                return render(request, "students/detail.html", {"form": form})

            student.user.username = form.cleaned_data["username"]
            student.user.first_name = form.cleaned_data["first_name"]
            student.user.last_name = form.cleaned_data["last_name"]
            student.settings = form.cleaned_data["settings"]
            student.user.save()
            student.save()

            return HttpResponseRedirect(f"/students/{student_id}/")
        else:
            return render(request, "students/detail.html", {"form": form})

    form = EditStudentForm(
        {
            "username": student.user.username,
            "first_name": student.user.first_name,
            "last_name": student.user.last_name,
            "group": student.group.number,
            "telegram_id": student.telegram_id,
            "settings": json.dumps(student.settings),
        }
    )

    return render(request, "students/detail.html", {"form": form})
