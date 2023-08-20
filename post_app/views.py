from django.shortcuts import render
from django.http import JsonResponse
from .models import Sub_Category
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def post_detail(request, pk):

    return render(request, 'Post/detail.html', {})


def post_create(request):
    return render(request,'Post/create.html',{})

@csrf_exempt
def get_subcategories(request):
    category_id = request.GET.get('category_id')

    if category_id:
        subcategories = Sub_Category.objects.filter(category_id=category_id).values('id', 'name')
        subcategories_dict = {subcategory['id']: subcategory['name'] for subcategory in subcategories}
        return JsonResponse(subcategories_dict)

    return JsonResponse({})
