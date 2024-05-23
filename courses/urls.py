from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('courses/', views.courses, name='courses'),  
    path('register/', views.register, name = 'register'),
    path('add_student/', views.add_student, name = 'add_student'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
    path('reg_course/<str:code>', views.reg_course, name='reg_course'),
    path('student_courses/', views.student_courses, name='student_courses'),
    path('unreg_course/<str:code>/', views.unreg_course, name='unreg_course'),
    path('course_enrollment_report/', views.course_enrollment_report, name='course_enrollment_report'),
    path('notifications/', views.notifications, name='notifications'),

]