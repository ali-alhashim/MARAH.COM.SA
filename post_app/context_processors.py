from .models import Post_Category, Location

def categories_list(request):
    categories = Post_Category.objects.all().values('name','id')
    return dict(categories=categories)

def location_list(request):
    location = Location.objects.all().values('name','id')
    return dict(location=location)
