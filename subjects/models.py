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
        through='subjects.Enrollment',
        related_name='student_subjects',
    )

    def __str__(self) -> str:
        return f'{self.code} - {self.name}'

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


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments'
    )
    subject = models.ForeignKey(
        'subjects.Subject', on_delete=models.CASCADE, related_name='enrollments'
    )
    enrolled_at = models.DateField(auto_now_add=True)
    mark = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.student}, enrolled at {self.enrolled_at} in {self.subject}'

    def get_mark_value(self) -> str:
        return self.mark if self.mark != None else ''
