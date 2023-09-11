from django.core.management import BaseCommand
from post_app.models import Post_Category, Sub_Category

class Command(BaseCommand):
    # Show this when the user types help
    help = "loads default  Categories & sub Categories "
    def handle(self, *args, **options):
        categories = [
            {
                'name': 'مراح الابل',
                'subcategories': [
                    {'name': 'المجاهيم'},
                    {'name': 'المغاتير'},
                    {'name': 'الهجن'},
                    {'name': 'المزايين'},
                    {'name': 'حشوان'},
                    {'name': 'الفحول'},
                    {'name': 'مستلزمات الابل'},
                    {'name': 'منتجات الابل'},
                ]
            },
            {
                'name': 'مراح الأغنام',
                'subcategories': [
                    {'name': 'الضأن'},
                    {'name': 'الماعز'},
                    {'name': 'حري'},
                    {'name': 'سواكني'},
                    {'name': 'بربري'},
                    {'name': 'مستورد'},
                    {'name': 'منتجات الأغنام'},
                    {'name': 'مستلزمات الأغنام'},
                ]
            },

             {
                'name': 'مراح الخيل',
                'subcategories': [
                    {'name': 'العربي'},
                    {'name': 'انجليزي'},
                    {'name': 'مصري'},
                    {'name': 'مستلزمات الخيل'},
                  
                ]
            },

            {
                'name': 'مراح الأبقار',
                'subcategories': [
                    {'name': 'بلدي'},
                    {'name': 'هولندي'},
                    {'name': 'انجوس'},
                    {'name': ' جيرسي'},
                    {'name': ' سويسري'},
                    {'name': ' منتجات الأبقار'},
                     {'name': '  مستلزمات الأبقار'},
                  
                ]
            },

              {
                'name': 'مراح الصقور',
                'subcategories': [
                    {'name': 'حر'},
                    {'name': 'شاهين'},
                    {'name': 'جير'},
                    {'name': ' وكري'},
                    {'name': ' اخرى'},
                 
                     {'name': '  مستلزمات الصقور'},
                  
                ]
            },

             {
                'name': 'مراح الطيور',
                'subcategories': [
                    {'name': 'حمام'},
                    {'name': 'دجاج'},
                    {'name': 'ببغاء'},
                    {'name': ' بط'},
                    {'name': ' منتجات الطيور'},
                 
                     {'name': 'مستلزمات الطيور'},
                  
                ]
            },

             {
                'name': ' الأعلاف',
                'subcategories': [
                    {'name': 'الشعير'},
                    {'name': 'البرسيم'},
                    {'name': 'الرودس'},
                    {'name': ' مكملات غدائية'},
                    {'name': '  اعلاف مستوردة'},
                 
                     {'name': ' مبيدات الاعلاف'},
                    {'name': 'الآت و معدات الاعلاف'},
                  
                ]
            },

             {
                'name': ' البيطرة',
                'subcategories': [
                    {'name': 'بيطرة الابل'},
                    {'name': 'بيطرة الاغنام'},
                    {'name': 'بيطرة الابقار'},
                    {'name': '  بيطرة الخيول'},
                    {'name': '   بيطرة الصقور'},
                 
                     {'name': '  المراكز البيطرية'},
                 
                  
                ]
            },
        ]

        for category_data in categories:
            category_name = category_data['name']
            subcategories_data = category_data['subcategories']

            # Create category
            category = Post_Category.objects.create(name=category_name)

            # Create subcategories
            for subcategory_data in subcategories_data:
                subcategory_name = subcategory_data['name']
                Sub_Category.objects.create(name=subcategory_name, category=category)

        self.stdout.write(self.style.SUCCESS('Categories and subcategories created successfully.'))