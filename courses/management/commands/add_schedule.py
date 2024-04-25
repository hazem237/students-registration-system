from django.core.management.base import BaseCommand
from courses.models import CourseSchedule
import datetime

class Command(BaseCommand):
    help = 'Adds sample schedules to the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding sample schedules...'))

        CourseSchedule.objects.create(
            days='Sunday,Tuesday,Wednesday', 
            start_time=datetime.time(8, 0),  
            end_time=datetime.time(9, 0),  
            room_number='C316' 
        )

        self.stdout.write(self.style.SUCCESS('Sample schedules added successfully!'))
