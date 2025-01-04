from django_rq import job
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
from markdown import markdown
import datetime

@job
def deliver_certificate(base_url, student):
    rendered = render_to_string('subjects/certificate/certificate.html', dict(student=student, today=datetime.date.today()))
    output_path = settings.CERTIFICATE_DIR / f'{student.username}_grade_certificate.pdf'
    HTML(string=rendered, base_url=base_url).write_pdf(output_path)
    rendered = render_to_string('subjects/certificate/email.md', dict(student=student))
    email = EmailMessage(
        subject='Grade certificate',
        body=markdown(rendered),
        from_email='info@lumino.com',
        to=[student.email],
    )
    email.content_subtype = 'html'
    email.attach_file(output_path)
    email.send()