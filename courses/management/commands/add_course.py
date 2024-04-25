from django.core.management.base import BaseCommand

from courses.models import Course

class Command(BaseCommand):
    help = 'Adds sample courses to the database'

    def handle(self):
        self.stdout.write(self.style.SUCCESS('Adding sample courses...'))

        Course.objects.create(
            code='CS102',
            name='Introduction to Computer Science',
            description='This course provides an introduction to computer science concepts...',
            instructor='Prof. Smith',
            capacity=30,
            schedule_id=2
        )

        self.stdout.write(self.style.SUCCESS('Sample courses added successfully!'))