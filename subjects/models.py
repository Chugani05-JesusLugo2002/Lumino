from django.conf import settings
from django.db import models


class Subject(models.Model):
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subjects'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='users.Enrollment', related_name='subjects'
    )


class Lesson(models.Model):
    subject = models.OneToOneField('subjects.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
