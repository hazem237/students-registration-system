from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from courses.forms import UserRegestraionForm
from .models import Course, Deadline, Notification, Student, StudentRegistration
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def courses(request, code=None):
    user_id = request.user.id
    student = Student.objects.get(user_id=user_id)
    
    registered_courses = StudentRegistration.objects.filter(student=student).values_list('course__code', flat=True)
    
    available_courses = Course.objects.exclude(code__in=registered_courses)
    
    eligible_courses = available_courses.filter(pre_requisites__isnull=True) | available_courses.filter(pre_requisites__code__in=registered_courses)
    
    eligible_courses = Course.objects.filter(pk__in=[course.pk for course in eligible_courses])
    
    query = request.GET.get('q')
    if query:
        eligible_courses = eligible_courses.filter(name__icontains=query) | eligible_courses.filter(code__icontains=query) | eligible_courses.filter(description__icontains=query)
    
    return render(request, 'course_list.html', {'courses': eligible_courses, 'reg_courses': registered_courses})


def register(request):
    error = ''
    form = UserRegestraionForm()
    if request.method == 'POST':
        form = UserRegestraionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            error = 'invalid data'
    return render(request, 'registration.html', {'form': form, 'error': error})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'invalid username or password'})
    return render(request, 'login.html', )

@login_required
def user_logout(request):
    if request.user:
        logout(request)
    return redirect('login')

@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        major = request.POST.get('major')
        avg = request.POST.get('avg')
        student = Student()
        student.name = name
        student.major = major
        student.avg = avg
        student.user = request.user
        student.save()
        return redirect('home')
    return render(request, 'student_form.html')

@login_required
def reg_course(request, code):
    user_id = request.user.id
    student = Student.objects.get(user_id=user_id)
    course = get_object_or_404(Course, code=code)

    current_registrations = StudentRegistration.objects.filter(course=course).count()
    if current_registrations >= course.capacity:
        messages.error(request, 'The course is full. You cannot register for this course.')
        return redirect('courses')

    student_courses = StudentRegistration.objects.filter(student=student)
    new_course_schedule = course.schedule

    for student_course in student_courses:
        student_course_schedule = student_course.course.schedule
        if (student_course_schedule.days == new_course_schedule.days and
            student_course_schedule.start_time < new_course_schedule.end_time and
            new_course_schedule.start_time < student_course_schedule.end_time):
            messages.error(request, 'Schedule conflict detected with another registered course. You cannot register for this course.')
            return redirect('courses')

    student_reg = StudentRegistration(student=student, course=course)
    student_reg.save()
    
    reg_courses = request.session.get('reg_courses', [])
    reg_courses.append(code)
    request.session['reg_courses'] = reg_courses

    messages.success(request, 'You have successfully registered for the course.')
    
    return redirect('student_courses')

@login_required
def student_courses(request):
    user_id = request.user.id
    student = Student.objects.get(user_id = user_id)
    student_courses_list = StudentRegistration.objects.filter(student = student)
    courses = []
    for reg in student_courses_list:
        courses.append(reg.course)
    return render(request, 'student_courses.html', {'courses': courses})

@login_required
def unreg_course(request, code):
    user_id = request.user.id
    student = Student.objects.get(user_id = user_id)
    course = Course.objects.get(code=code)
    StudentRegistration.objects.filter(course = course, student = student).delete()
    return redirect('student_courses')


@login_required
def course_enrollment_report(request):
    course_enrollment = Course.objects.annotate(enrollment_count=Count('studentregistration')).order_by('-enrollment_count')
    total_enrollments = StudentRegistration.objects.count()
    most_popular_course = course_enrollment.first()
    courses = [course.name for course in course_enrollment]
    enrollments = [course.enrollment_count for course in course_enrollment]

    fig, ax = plt.subplots()
    ax.bar(courses, enrollments)
    ax.set_xlabel('Courses')
    ax.set_ylabel('Enrollments')
    ax.set_title('Course Enrollment Report')
    plt.xticks(rotation=90)

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    chart = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    context = {
        'course_enrollment': course_enrollment,
        'total_enrollments': total_enrollments,
        'most_popular_course': most_popular_course,
        'chart': chart,
    }
    return render(request, 'course_enrollment_report.html', context)

@receiver(post_save, sender=Deadline)
def send_notification_on_deadline_creation(sender, instance, created, **kwargs):
    if created:
        message = f'new message from admin: {instance.description}'
        if instance.type == 'course_deadline' and instance.course:
            registrations = StudentRegistration.objects.filter(course=instance.course)
            users = [reg.student.user for reg in registrations]
        else:
            users = User.objects.all()
        for user in users:
            Notification.objects.create(user=user, message=message)

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})
