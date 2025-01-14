from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    DEFAULT_AVATAR_URL = 'avatars/noavatar.png'

    class Role(models.TextChoices):
        STUDENT = 'S', 'Student'
        TEACHER = 'T', 'Teacher'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=Role, default=Role.STUDENT)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(
        blank=True, null=True, upload_to='avatars', default=DEFAULT_AVATAR_URL
    )

    @property
    def is_student(self) -> bool:
        return self.role == Profile.Role.STUDENT

    def __str__(self) -> str:
        return f'{self.get_role_display()} {self.user.first_name.title()} {self.user.last_name.title()}'

    def get_subjects(self):
        return self.user.enrolled.all() if self.is_student else self.user.taught.all()

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'username': self.user})

    def can_request_certificate(self) -> bool:
        have_enrolls = self.user.enrollments.all().count() > 0
        have_all_marks = self.user.enrollments.filter(mark=None).count() == 0
        return self.is_student and have_enrolls and have_all_marks
