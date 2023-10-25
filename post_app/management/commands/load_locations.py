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
                'latitude_start':24.6667,
                'latitude_end':24.6667,
                'longitude_start':47.2 ,
                'longitude_end':47.2 ,
               
            },
             {
                'name': 'ابها',
                'latitude_start':18.2134,
                'latitude_end':18.2134,
                'longitude_start':42.5000 ,
                'longitude_end':42.5000,
               
            },
             {
                'name': 'نجران',
                'latitude_start':17.5475,
                'latitude_end':17.5837,
                'longitude_start':44.2108 ,
                'longitude_end':44.2469,
               
            },
             {
                "name": "عرعر",
                "latitude_start": 26.39270,
                "latitude_end": 26.44670,
                "longitude_start": 49.98250,
                "longitude_end": 50.15000
            },
            {
                "name": "سكاكا",
                "latitude_start": 29.95389,
                "latitude_end": 29.99667,
                "longitude_start": 39.11472,
                "longitude_end": 39.19939
            },

              {
               "name": "جدة",
                "latitude_start": 21.34942,
                "latitude_end": 21.59442,
                "longitude_start": 39.08121,
                "longitude_end": 39.24314
               
            },

               {
                 "name": "مكة",
                "latitude_start": 21.28917,
                "latitude_end": 21.44412,
                "longitude_start": 39.81387,
                "longitude_end": 39.90189
               
            },

              {
               "name": "المدينة المنورة",
                "latitude_start": 24.46391,
                "latitude_end": 24.57616,
                "longitude_start": 39.53448,
                "longitude_end": 39.65704
               
            },
             {
    "name": "سيهات",
    "latitude_start": 26.22758,
    "latitude_end": 26.24108,
    "longitude_start": 50.25444,
    "longitude_end": 50.27556
  },
  {
    "name": "الدوادمي",
    "latitude_start": 25.54528,
    "latitude_end": 25.55778,
    "longitude_start": 44.17778,
    "longitude_end": 44.19111
  },
  {
    "name": "الخفجي",
    "latitude_start": 28.68333,
    "latitude_end": 28.73333,
    "longitude_start": 48.20000,
    "longitude_end": 48.25000
  },
  {
    "name": "طبرجل",
    "latitude_start": 29.72778,
    "latitude_end": 29.73889,
    "longitude_start": 43.25278,
    "longitude_end": 43.26528
  },
  {
    "name": "وادي الدواسر",
    "latitude_start": 23.06667,
    "latitude_end": 23.11667,
    "longitude_start": 44.00000,
    "longitude_end": 44.05000
  },
  {
    "name": "ينبع",
    "latitude_start": 23.78333,
    "latitude_end": 23.81667,
    "longitude_start": 38.70000,
    "longitude_end": 38.75000
  },
  {
    "name": "بقيق",
    "latitude_start": 26.25000,
    "latitude_end": 26.27500,
    "longitude_start": 49.80000,
    "longitude_end": 49.82500
  },

            {
    "name": "الطائف",
    "latitude_start": 21.24833,
    "latitude_end": 21.34833,
    "longitude_start": 40.29248,
    "longitude_end": 40.44383
  },
   {
    "name": "الهفوف",
    "latitude_start": 25.34772,
    "latitude_end": 25.55522,
    "longitude_start": 49.52555,
    "longitude_end": 49.79028
  },
  {
    "name": "خميس مشيط",
    "latitude_start": 18.28737,
    "latitude_end": 18.38362,
    "longitude_start": 42.66894,
    "longitude_end": 42.79191
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