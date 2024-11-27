from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit-profile'),
    path('certificate/', views.request_certificate, name='request-certificate'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('leave/', views.leave, name='leave'),
]
