# Generated by Django 5.0.4 on 2024-05-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_courseschedule_room_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseschedule',
            name='days',
            field=models.CharField(choices=[('sunday, tuesday, thursday', 'sunday, tuesday, thursday'), ('monday, wednesday', 'monday, wednesday')], max_length=100),
        ),
        migrations.AlterField(
            model_name='courseschedule',
            name='room_number',
            field=models.CharField(max_length=100),
        ),
    ]