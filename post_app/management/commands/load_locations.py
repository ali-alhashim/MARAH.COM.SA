from django.core.management import BaseCommand
from post_app.models import  Location

class Command(BaseCommand):
    # Show this when the user types help
    help = "loads default  locations "
    def handle(self, *args, **options):
        locations = [
            {
                'name': 'الرياض',
                'latitude_start':24.71667,
                'latitude_end':25.11667,
                'longitude_start':46.71667 ,
                'longitude_end':46.98333,
               
            },
             {
                'name': 'الدمام',
                'latitude_start':26.21667,
                'latitude_end':26.38333,
                'longitude_start':50.06667 ,
                'longitude_end':50.23333,
               
            },
             {
                'name': 'حفر الباطن',
                'latitude_start':31.16667,
                'latitude_end':31.33333,
                'longitude_start':44.93333 ,
                'longitude_end':45.13333,
               
            },
             {
                'name': 'نعيرية',
                'latitude_start':26.83333,
                'latitude_end':26.93333,
                'longitude_start':46.08333 ,
                'longitude_end':46.18333,
               
            },

             {
                'name': 'الجوف',
                'latitude_start':29.51667,
                'latitude_end': 30.51667,
                'longitude_start':39.08333 ,
                'longitude_end':40.08333,
               
            },
             {
                'name': 'القصيم',
                'latitude_start':26.16667,
                'latitude_end':27.16667,
                'longitude_start':43.08333 ,
                'longitude_end':44.08333,
               
            },
             {
                'name': 'الخبر',
                'latitude_start':26.28333,
                'latitude_end':26.38333,
                'longitude_start':49.93333 ,
                'longitude_end':50.03333,
               
            },

             {
                'name': 'الظهران',
                'latitude_start': 26.28333,
                'latitude_end': 26.31667,
                'longitude_start':50.08333 ,
                'longitude_end':50.11667,
               
            },
             {
                'name': 'الجبيل',
                'latitude_start':26.63333,
                'latitude_end':26.66667,
                'longitude_start':49.95667 ,
                'longitude_end':49.99667,
               
            },
             {
                'name': 'القطيف',
                'latitude_start':26.41667,
                'latitude_end':26.6,
                'longitude_start':49.86667 ,
                'longitude_end':50.1,
               
            },
             {
                'name': 'راس تنورة',
                'latitude_start':26.612556,
                'latitude_end': 26.648556,
                'longitude_start':50.163389 ,
                'longitude_end': 50.199389,
               
            },
             {
                'name': 'الأحساء',
                'latitude_start':25.20,
                'latitude_end':25.40,
                'longitude_start':49.50 ,
                'longitude_end':50.70,
               
            },
             {
                'name': 'بريدة',
                'latitude_start':26.29667 ,
                'latitude_end':26.33667,
                'longitude_start':43.96333  ,
                'longitude_end': 44.00333,
               
            },
             {
                'name': 'حايل',
                'latitude_start':27.50667,
                'latitude_end':27.52667,
                'longitude_start':41.69333 ,
                'longitude_end':41.71333,
               
            },
               ## part 1
            
             {
                'name': 'الخرج',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },
             {
                'name': 'ابها',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },
             {
                'name': 'نجران',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },
             {
                'name': 'عرعر',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },

            {
                'name': 'سكاكا',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },

              {
                'name': 'جدة',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },

               {
                'name': 'مكة',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },

              {
                'name': 'المدينة',
                'latitude_start':26.3927,
                'latitude_end':26.4467,
                'longitude_start':49.9825 ,
                'longitude_end':50.1500,
               
            },
           
        ]

        for location in locations:
            name           = location['name']
            latitude_start = location['latitude_start']
            latitude_end   = location['latitude_end']
            longitude_start= location['longitude_start']
            longitude_end  = location['longitude_end']

            # Create category
            Location.objects.create(name           =name,
                                    latitude_start = latitude_start,
                                    latitude_end   = latitude_end,
                                    longitude_start= longitude_start,
                                    longitude_end  = longitude_end
                                    )

           

        self.stdout.write(self.style.SUCCESS('Locations created successfully.'))