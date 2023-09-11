from django.core.management import BaseCommand
from post_app.models import Post_Category, Sub_Category

class Command(BaseCommand):
    # Show this when the user types help
    help = "loads default  Categories & sub Categories "
    def handle(self, *args, **options):
        categories = [
            {
                'name': 'Category 1',
                'subcategories': [
                    {'name': 'Subcategory 1'},
                    {'name': 'Subcategory 2'},
                ]
            },
            {
                'name': 'Category 2',
                'subcategories': [
                    {'name': 'Subcategory 3'},
                    {'name': 'Subcategory 4'},
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