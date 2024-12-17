# Generated by Django 5.1.3 on 2024-12-17 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0004_enrollment_alter_subject_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teacher_subjects', to=settings.AUTH_USER_MODEL),
        ),
    ]
