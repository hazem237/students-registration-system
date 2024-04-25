
from django.shortcuts import render
from .models import Course, CourseSchedule

def course_list_view(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})


def schedule_list_view(request):
    schedules = CourseSchedule.objects.all()
    return render(request, 'schedule_list.html', {'schedules': schedules})
