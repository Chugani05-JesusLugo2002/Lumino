from django.conf import settings
from django.db import models


class Profile(models.Model):
    STUDENT = 'S'
    TEACHER = 'T'
    ROLES_CHOICES = {STUDENT: 'Student', TEACHER: 'Teacher'}

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLES_CHOICES, default=STUDENT)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars', default='avatars/noavatar.png'
    )


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='enrollments'
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.IntegerField(null=True)
