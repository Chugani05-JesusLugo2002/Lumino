from django.conf import settings
from django.db import models
from django.urls import reverse


class Subject(models.Model):
    code = models.CharField(unique=True, max_length=3)
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_subjects'
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='users.Enrollment',
        related_name='student_subjects',
    )

    def __str__(self) -> str:
        return f'{self.name} ({self.code}), imparted by {self.teacher}'

    def get_absolute_url(self):
        return reverse('subjects:subject-detail', kwargs={'subject_code': self.code})


class Lesson(models.Model):
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='lessons'
    )
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse(
            'subjects:lesson-detail',
            kwargs={'subject_code': self.subject.code, 'lesson_pk': self.pk},
        )
