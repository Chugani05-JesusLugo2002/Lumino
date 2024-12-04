from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit-profile'),
    path('certificate/', views.request_certificate, name='request-certificate'),
    path('leave/', views.leave, name='leave'),
]
