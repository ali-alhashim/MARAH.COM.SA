from .models import Post_Category

def categories_list(request):
    categories = Post_Category.objects.all().values('name','id')
    return dict(categories=categories)
