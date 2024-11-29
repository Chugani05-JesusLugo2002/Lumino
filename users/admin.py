from django.contrib import admin

from .models import Profile, Enrollment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    pass