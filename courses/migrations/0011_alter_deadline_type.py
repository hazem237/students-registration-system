# Generated by Django 5.0.4 on 2024-05-22 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deadline',
            name='type',
            field=models.CharField(choices=[('registration', 'Registration Deadline'), ('drop_add', 'Drop/Add Deadline'), ('course_deadline', 'Course Deadline')], max_length=20),
        ),
    ]