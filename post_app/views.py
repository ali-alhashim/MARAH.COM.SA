from django.shortcuts import render

# Create your views here.

def post_detail(request, pk):

    return render(request, 'Post/detail.html', {})
