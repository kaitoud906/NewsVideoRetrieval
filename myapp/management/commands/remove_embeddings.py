from django.core.management.base import BaseCommand
from myapp.models import ImageEmbedding 

class Command(BaseCommand):
    help = 'Remove all records from a specific database table'

    def handle(self, *args, **options):
        try:
            ImageEmbedding.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('All records removed successfully.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
