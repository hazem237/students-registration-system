from django.db import models

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.EmailField(unique=True)

class Course(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField()
    pre_requisites = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.CharField(max_length=32)
    capacity = models.PositiveIntegerField()
    schedule = models.ForeignKey('CourseSchedule', on_delete=models.CASCADE)

class StudentRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class CourseSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    DAY_CHOICES = [
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]
    days = models.CharField(max_length=50, choices=DAY_CHOICES, help_text="Select multiple days for the course schedule", null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20)