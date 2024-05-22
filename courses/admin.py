from django.contrib import admin

from courses.models import Course, CourseSchedule, Deadline, Notification, Student, StudentRegistration

# Register your models here.

admin.site.register(CourseSchedule),
admin.site.register(StudentRegistration),
admin.site.register(Course),
admin.site.register(Student),
admin.site.register(Notification),

class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('description', 'deadline_date')
    search_fields = ('description',)

admin.site.register(Deadline, DeadlineAdmin)

