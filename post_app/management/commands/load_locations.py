from django.core.management import BaseCommand
from post_app.models import  Location

class Command(BaseCommand):
    # Show this when the user types help
    help = "loads default  locations "
    def handle(self, *args, **options):
        locations = [
            {
                'name': 'الرياض',
               
            },
             {
                'name': 'الدمام',
               
            },
             {
                'name': 'حفر الباطن',
               
            },
             {
                'name': 'نعيرية',
               
            },
             {
                'name': 'الجوف',
               
            },
             {
                'name': 'القصيم',
               
            },
             {
                'name': 'الخبر',
               
            },
             {
                'name': 'الظهران',
               
            },
             {
                'name': 'الجبيل',
               
            },
             {
                'name': 'القطيف',
               
            },
             {
                'name': 'راس تنورة',
               
            },
             {
                'name': 'الأحساء',
               
            },
             {
                'name': 'بريدة',
               
            },
             {
                'name': 'حايل',
               
            },
             {
                'name': 'الخرج',
               
            },
             {
                'name': 'ابها',
               
            },
             {
                'name': 'نجران',
               
            },
             {
                'name': 'عرعر',
               
            },
           
        ]

        for location in locations:
            location = location['name']
          

            # Create category
            Location.objects.create(name=location)

           

        self.stdout.write(self.style.SUCCESS('Locations created successfully.'))