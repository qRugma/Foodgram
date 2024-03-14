import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


class Command(BaseCommand):
    help = (
        'Load Ingredient model '
        'from file ingredient.csv in django root.'
    )

    def handle(self, *args, **options):
        file = open('ingredients.csv', 'r', encoding='UTF-8')
        spamreader = csv.reader(file, delimiter=',', quotechar='|')
        for row in spamreader:
            Ingredient.objects.create(
                name=row[0],
                measurement_unit=row[1],
            )
        print('done')
