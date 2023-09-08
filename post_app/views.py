from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Sub_Category, Post_Category, Post, Location, Post_Images, Post_Comment, MyFavorite,Post_Complaints
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.

def post_detail(request, pk):
    thePost = Post.objects.get(pk=pk)
    if request.user.is_authenticated:
        Userfavorite = MyFavorite.objects.filter(post=thePost, user=request.user).exists()
    else:
        Userfavorite = False
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
            return redirect('post.detail', pk=pk)
        else:
            print('you must login before you post your comment')
            return HttpResponseRedirect(reverse_lazy('login'))
    return render(request, 'Post/detail.html', {"thePost":thePost,"Userfavorite":Userfavorite})






def post_create(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'يجب عليك تسجيل الدخول حتى تتمكن من إضافة إعلان')
        return HttpResponseRedirect(reverse_lazy('login'))
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
        counter = 0
        for image in uploaded_images:
            postImage = Post_Images(
                                    post  = newPost,
                                    image = image
                                    )
             # Save the image to a file
            postImage.image.save(image.name, image)
            postImage.save()
            counter = counter + 1
            if counter == 10:
                break
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





def MyPosts(request):
    print('Start Search View....')
    category  = request.GET.get('category')
    searchKey = request.GET.get('searchKey')
    selectedLocation  = request.GET.get('location')

    query = Q()
    print('location:', selectedLocation)
    if selectedLocation != 'all' and selectedLocation is not None:
       
        locationObj = Location.objects.get(pk=selectedLocation)
        print('you select location ', locationObj.name)
        query = Q(location = locationObj)
        selectedLocation = locationObj
    else:
        selectedLocation ='all'

    if category !='all' and category is not None:
        categoryObj = Post_Category.objects.get(pk=category)
        category = categoryObj
        query &= Q(category = categoryObj)
    else:
        category ='all'

    print('your query = ', query)
    posts = Post.objects.filter(query & Q(created_by = request.user)).order_by('-created_date')
    return render(request,'Post/MyPosts/list.html',{"posts":posts,"selectedLocation":selectedLocation,"selectedcategory":category})



def MyFavorite_List(request):
    category  = request.GET.get('category')
    searchKey = request.GET.get('searchKey')
    selectedLocation  = request.GET.get('location')

    query = Q()
    print('location:', selectedLocation)
    if selectedLocation != 'all' and selectedLocation is not None:
       
        locationObj = Location.objects.get(pk=selectedLocation)
        print('you select location ', locationObj.name)
        query = Q(location = locationObj)
        selectedLocation = locationObj
    else:
        selectedLocation ='all'

    if category !='all' and category is not None:
        categoryObj = Post_Category.objects.get(pk=category)
        category = categoryObj
        query &= Q(category = categoryObj)
    else:
        category ='all'

    favoriteList = MyFavorite.objects.filter(user=request.user)
    
    return render(request,'User/MyFavorite/list.html',{"favoriteList":favoriteList,"selectedLocation":selectedLocation,"selectedcategory":category})



def Post_Complaints_Create(request):
    if request.method=="POST":
        subject = request.POST.get('subject')
        post_id = request.POST.get('post_id')
        message = request.POST.get('message')
        thePost = Post.objects.get(pk=post_id)
        if request.user.is_authenticated:
            newComplain = Post_Complaints(
                                        user = request.user,
                                        post = thePost,
                                        subject = subject,
                                        message = message
                                        )
            newComplain.save()
            messages.success(request, 'تم إستلام البلاغ شكراً')
            return redirect('post.detail', pk=post_id)
        else:
            messages.error(request,'يجب عليك تسجيل الدخول أولاً')
            return redirect('login')
        


def deletePost(request,postId):
    thePost = Post.objects.get(pk=postId)
    if thePost.created_by == request.user:
        thePost.delete()
        messages.success(request,'تم حذف الإعلان')
    else:
        messages.error(request, ' لا تملك الصلاحية لحذف هذا الإعلان')
    return redirect('My.Posts')




def updatePost(request, postId):
    thePost = Post.objects.get(pk=postId)
    if thePost.created_by ==request.user:
        if request.method=="POST":
            print('get the update values')

            location     = Location.objects.get(pk=int(request.POST.get('location')))
            category     = Post_Category.objects.get(pk=int(request.POST.get('category')))
            sub_category = Sub_Category.objects.get(pk=int(request.POST.get('sub_category')))
            subject      = request.POST.get('subject')
            text         = request.POST.get('text')

            thePost.text         = text
            thePost.subject      = subject
            thePost.category     = category
            thePost.location     = location
            thePost.sub_category = sub_category
            thePost.save()

            messages.success(request,'تم تعديل الإعلان')
            return redirect('My.Posts')
        return render(request, 'Post/MyPosts/update.html',{"post":thePost})
    else:
        messages.error(request, ' لا تملك الصلاحية لــ تعديل هذا الإعلان')
        return redirect('home')
        






