from django.core.management.base import BaseCommand

from subjects.models import Subject

class Command(BaseCommand):
    help = 'Show average marks from all subjects.'

    def handle(self, *args, **options):
        for subject in Subject.objects.all():
            enrolls = subject.enrollments.exclude(mark=None)
            length = enrolls.count()
            if length > 0:
                average_mark = sum([enroll.mark for enroll in enrolls]) / length
                self.stdout.write(f'{subject.code}: {average_mark:.2f}')