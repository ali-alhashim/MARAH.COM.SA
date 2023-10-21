from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import Sub_Category, Post_Category, Post, Location, Post_Images, Post_Comment, MyFavorite,Post_Complaints
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
from django.db.models import Count
from django.db.models.functions import Coalesce
import math
import os
import shutil
from django.conf import settings
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
    totalMyPost = posts.count()
    ### Paginator ----
    items_per_page = 10
    paginator = Paginator(posts, items_per_page)
    page = paginator.get_page(1)
    return render(request,'Post/MyPosts/list.html',{"posts":page,"selectedLocation":selectedLocation,"selectedcategory":category,"totalMyPost":totalMyPost})


################# load More MyPosts

def MyPosts_loadMore(request):
    page_number = request.GET.get('page_number')
    print('load more page #', page_number)
    items_per_page = 10

    comment_count_subquery = Post_Comment.objects.filter(post=OuterRef('id')).values('post').annotate(comment_count=Coalesce(Count('id'), 0)).values('comment_count')
    
    image_subquery = Post_Images.objects.filter(post=OuterRef('id')).order_by('id').values('image')[:1]
    

    posts = Post.objects.filter(created_by=request.user).order_by('-created_date').annotate(comment_count=Subquery(comment_count_subquery), first_image=Subquery(image_subquery)).values('id', 'subject', 'category__name', 'sub_category__name', 'location__name', 'created_date', 'created_by__name', 'comment_count', 'first_image')
    paginator = Paginator(posts, items_per_page)

    print("get page #", page_number)
    page = paginator.get_page(page_number)

    Totalposts = Post.objects.filter(created_by=request.user).count()
   
    totalPages = math.ceil(Totalposts / 10)
    print(totalPages)


    if int(page_number) > totalPages:
        page = {"End"}
    else:
            # Convert QuerySet to list and replace 'null' with 0 for comment_count
        page_list = list(page)
        for item in page_list:
            item['comment_count'] = item['comment_count'] or 0

     
   
    return JsonResponse(list(page), safe=False)

################


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
        ## delete also the photo
        folder_path = os.path.join(settings.MEDIA_ROOT, f"post_images/{postId}")
        try:
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' and its contents have been deleted.")
        except FileNotFoundError:
            print(f"Folder '{folder_path}' does not exist.")
        except PermissionError:
            print(f"Permission denied: Unable to delete folder '{folder_path}'.")
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

            ## convert str to list and delete all img by ids
            if 'deleted_img' in request.POST and request.POST.get('deleted_img'):
                deleted_img  = request.POST.get('deleted_img')
                imgId_list = deleted_img.split(",")
                for imgId in imgId_list:
                    theImage = Post_Images.objects.get(pk=int(imgId))
                    theImage.delete()
            ## check if user want's to add photo, check post total photo after delete and let him add not more than 10
            ## count the exist photo for this post
            existImgs = thePost.post_images.all().count()
            if existImgs < 10:
                 ## upload post images
                uploaded_images = request.FILES.getlist('photos')
                counter = existImgs
                for image in uploaded_images:
                    postImage = Post_Images(
                                            post  = thePost,
                                            image = image
                                            )
                    # Save the image to a file
                    postImage.image.save(image.name, image)
                    postImage.save()
                    counter = counter + 1
                    if counter == 10:
                        break

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
        






