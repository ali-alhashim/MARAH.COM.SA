from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .models import Sub_Category, Post_Category, Post, Location, Post_Images, Post_Comment
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.

def post_detail(request, pk):
    thePost = Post.objects.get(pk=pk)
    if request.method == "POST":
        print('check befor you post comment if the user authenticated')
        if request.user.is_authenticated:
            comment = request.POST.get('comment')
            newComment = Post_Comment(
                                    post = thePost,
                                    created_by = request.user,
                                    comment    = comment
                                    )
            newComment.save()
        else:
            print('you must login before you post your comment')
            return HttpResponseRedirect(reverse_lazy('login'))
    return render(request, 'Post/detail.html', {"thePost":thePost})


def post_create(request):
    if request.method == "POST":
        category     = Post_Category.objects.get(pk=request.POST.get('category'))
        sub_category = Sub_Category.objects.get(pk=request.POST.get('sub_category'))
        location     = Location.objects.get(pk=request.POST.get('location'))
        newPost = Post(
                        created_by   = request.user,
                        subject      = request.POST.get('subject'),
                        text         = request.POST.get('text'),
                        location     = location,
                        category     = category,
                        sub_category = sub_category,
                      )
        newPost.save()
        ## upload post images
        uploaded_images = request.FILES.getlist('photos')
        for image in uploaded_images:
            postImage = Post_Images(
                                    post  = newPost,
                                    image = image
                                    )
             # Save the image to a file
            postImage.image.save(image.name, image)
            postImage.save()
        return HttpResponseRedirect(reverse_lazy('post.detail',kwargs={'pk':newPost.id}))
    
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



