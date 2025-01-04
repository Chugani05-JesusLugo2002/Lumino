from django.conf import settings
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=Role, default=Role.STUDENT)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars', default='avatars/noavatar.png'
    )

    @property
    def is_student(self) -> bool:
        return self.role == Profile.Role.STUDENT

    def can_request_certificate(self) -> bool:
        return self.is_student and self.user.enrollments.all().count() > 0 and self.user.enrollments.filter(mark=None).count() == 0

    def __str__(self) -> str:
        return f'{self.role}: {self.user}'

    def get_subjects(self):
        if self.is_student:
            return self.user.enrolled.all()
        return self.user.teacher_subjects.all()
