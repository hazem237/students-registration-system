# Generated by Django 5.0.4 on 2024-05-19 12:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_courseschedule_days_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
        migrations.AddField(
            model_name='student',
            name='avg',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='major',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
