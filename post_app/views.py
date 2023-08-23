from django.shortcuts import render
from django.http import JsonResponse
from .models import Sub_Category, Post_Category
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def post_detail(request, pk):

    return render(request, 'Post/detail.html', {})


def post_create(request):
    return render(request,'Post/create.html',{})


@csrf_exempt
def get_subcategories(request):
    category_id = request.GET.get('category_id')
    print('you call get sub category', category_id)
    if category_id:
        category = Post_Category.objects.get(pk=category_id)
        subcategories = list(Sub_Category.objects.filter(category=category).values('id', 'name'))
        
        return JsonResponse(subcategories, safe=False)

    return JsonResponse({})



