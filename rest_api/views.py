from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import  OuterRef, Subquery
from post_app.models import Post, Location, Post_Images, Post_Category

# Create your views here.

### http://127.0.0.1:8000/api/posts/list
def api_posts_list(request):
    subquery = Post_Images.objects.filter(post=OuterRef('id')).order_by('created_date')
    data = (Post.objects.annotate(first_image=Subquery(subquery.values('image')[:1]))
            .values("id", "subject", "created_by", "location", "category", "created_date", "first_image")
            )
        
    
    return JsonResponse(list(data), safe=False)



### http://127.0.0.1:8000/api/locations

def api_locations(request):
    data = list(Location.objects.all().values("id","name"))
    return JsonResponse(data, safe=False)


### http://127.0.0.1:8000/api/categories

def api_categories(request):
    data = list(Post_Category.objects.all().values("id","name"))
    return JsonResponse(data, safe=False)