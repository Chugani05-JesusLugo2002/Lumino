from django.contrib import admin

from .models import Enrollment, Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass
