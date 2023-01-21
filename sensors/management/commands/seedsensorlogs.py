from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
from sensors.models import Sensor
from sensors.models import SensorLog
import random

class Command(BaseCommand):
    help = 'Seeds database with sample SensorLogs'

    def add_arguments(self, parser):
        parser.add_argument('number', nargs='+', type=int)

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        seeder.add_entity(SensorLog, options['number'][0], {
            'sensor': lambda x: Sensor.objects.get(pk=random.randint(1, 2)),
            'temperature': lambda x: random.uniform(-20, 30),
            'humidity': lambda x: random.uniform(20, 80),
            'pressure': lambda x: random.uniform(990, 1050),
            'altitude': lambda x: random.uniform(150, 200),
        })

        print(seeder.execute())