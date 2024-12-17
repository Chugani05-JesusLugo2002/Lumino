from django.urls import path

from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('enroll/', views.enroll_subjects, name='enroll-subjects'),
    path('unenroll/', views.unenroll_subjects, name='unenroll-subjects'),
    path('certificate/', views.request_certificate, name='request-certificate'),
    path('<str:subject_code>/', views.subject_detail, name='subject-detail'),
    path('<str:subject_code>/lessons/add/', views.add_lesson, name='add-lesson'),
    path('<str:subject_code>/lessons/<int:lesson_pk>/', views.lesson_detail, name='lesson-detail'),
    path('<str:subject_code>/lessons/<int:lesson_pk>/edit/', views.edit_lesson, name='edit-lesson'),
    path(
        '<str:subject_code>/lessons/<int:lesson_pk>/delete/',
        views.delete_lesson,
        name='delete-lesson',
    ),
    path('<str:subject_code>/marks/', views.mark_list, name='mark-list'),
    path('<str:subject_code>/marks/edit', views.edit_marks, name='edit-marks'),
]
