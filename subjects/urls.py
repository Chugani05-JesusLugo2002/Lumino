from django.urls import path, re_path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('certificate/', views.request_certificate, name='request-certificate'),
    re_path(r'(?P<subject_code>[A-Z]{3})/$', views.subject_detail, name='subject-detail'),
    re_path(r'(?P<subject_code>[A-Z]{3})/lessons/add/$', views.add_lesson, name='add-lesson'),
    re_path(r'(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/$', views.lesson_detail, name='lesson-detail'),
    re_path(r'(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/edit/$', views.edit_lesson, name='edit-lesson'),
    re_path(
        r'(?P<subject_code>[A-Z]{3})/lessons/(?P<lesson_pk>\d+)/delete/$',
        views.delete_lesson,
        name='delete-lesson',
    ),
    re_path(r'(?P<subject_code>[A-Z]{3})/marks/$', views.mark_list, name='mark-list'),
    re_path(r'(?P<subject_code>[A-Z]{3})/marks/edit/$', views.edit_marks, name='edit-marks'),
]
