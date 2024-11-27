from django.contrib import admin

from .models import Lesson, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass
