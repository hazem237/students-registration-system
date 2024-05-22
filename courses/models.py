import datetime
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    name = models.CharField(max_length=32, null=True)
    major = models.CharField(max_length=100, null=True)
    avg = models.FloatField(null= True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField()
    pre_requisites = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    schedule = models.ForeignKey('CourseSchedule', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class StudentRegistration(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class CourseSchedule(models.Model):
    DAYS = (
        ('sunday, tuesday, thursday', 'sunday, tuesday, thursday'),
        ('monday, wednesday', 'monday, wednesday'),
    )
    days = models.CharField(max_length=100, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.get_days_display()} from {self.start_time} to {self.end_time} in room {self.room_number}"
    

class Deadline(models.Model):
    TYPE_CHOICES = (
        ('registration', 'Registration Deadline'),
        ('drop_add', 'Drop/Add Deadline'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    deadline_date = models.DateField()

    def __str__(self):
        return f'{self.get_type_display()} - {self.description}'
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


