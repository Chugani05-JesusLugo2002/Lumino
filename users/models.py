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

    def is_student(self):
        return True if self.role == Profile.Role.STUDENT else False

    def get_subject_list(self):
        if self.is_student():
            return self.user.student_subjects.all()
        return self.user.teacher_subjects.all()

    def __str__(self) -> str:
        return f'{self.role}: {self.user}'
