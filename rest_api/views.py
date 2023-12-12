from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import  OuterRef, Subquery
from post_app.models import Post, Location, Post_Images, Post_Category, Sub_Category, Post_Comment,MyFavorite
from django.contrib.auth import authenticate, login
from user_app.models import User
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

### http://127.0.0.1:8000/api/posts/list
def api_posts_list(request):
    items_per_page = 10
    subquery    = Post_Images.objects.filter(post=OuterRef('id')).order_by('created_date')
    
    getPage     = request.GET.get("page") # you want page number
    category    = request.GET.get("category") # you want to filter post with this category
    subcategory = request.GET.get("subcategory") # you want to filter with this subcategory
    location    = request.GET.get("location") # you want to filter with this location
    isInMyFavorite = request.GET.get("isInMyFavorite")
    username    = request.GET.get("username")
    token       = request.GET.get("token")

    query = Q()
    if int(category) !=0:
        print("category != 0")
        query |=Q(category__id=category)
    if int(location) !=0:
        query |=Q(location__id=location)

    
    posts = (Post.objects.filter(query).annotate(first_image=Subquery(subquery.values('image')[:1]))
            .values("id", "subject", "created_by__name", "location__name", "category__name", "sub_category__name", "created_date", "first_image")
            ).order_by("-last_update")
    
     # Convert created_date to a readable format
    for post in posts:
        post['created_date'] = post['created_date'].strftime("%B %d, %Y at %I:%M %p")

    #print(posts)
    paginator = Paginator(posts, items_per_page)
    page = paginator.get_page(1)   
    print('home page_number =>', 1) 
    
    return JsonResponse(list(page), safe=False)

## http://127.0.0.1:8000/api/add/comment
@csrf_exempt
def api_add_post_comment(request):
     response = ""
     if request.method =="POST":
         byUser     = request.POST.get("byUser")
         token      = request.POST.get("token")
         theComment = request.POST.get("theComment")
         postId     = request.POST.get("postId")

         thePost = Post.objects.get(pk=postId)
         theUser = User.objects.filter(name=byUser).first()
         if theUser:
             print("user exists check the token")
             if theUser.token == token:
                print("the token match so add the comment")
                newComment = Post_Comment(
                                            post = thePost,
                                            created_by = theUser,
                                            comment = theComment
                                         )
                newComment.save()
                response = {"status":"post comment has been added successfully "}
                return JsonResponse(response, safe=False) 

             else:
                 response = {"status":"token not match"}
                 print("token not match")
                 return JsonResponse(response, safe=False) 
         else:
             response = {"status":"the user not exist !"}
             return JsonResponse(response, safe=False)
             


        
     response = {"status":"only http post request !"}
     return JsonResponse(response, safe=False)

### http://127.0.0.1:8000/api/post/detail?postId=1
@csrf_exempt
def api_post_detail(request):
    if request.method =="GET":
        postId = request.GET.get("postId")
        username = request.GET.get("username")
        try:
            theUser = User.objects.get(name=username)
        except ObjectDoesNotExist:
            theUser = None
        
        thePost = Post.objects.get(pk=postId)
        postImages = Post_Images.objects.filter(post = thePost)

        isInMyFavorite = MyFavorite.objects.filter(post = thePost, user = theUser).exists()

        images = [image.image.url for image in postImages]

        postComments = Post_Comment.objects.filter(post = thePost)
        comments = []
        for comment in postComments:
            
            comment_data = {
                'comment_text': comment.comment,
                'comment_user': comment.get_created_by_name(),
                'created_date': comment.created_date.strftime("%B %d, %Y at %I:%M %p")
            }
            comments.append(comment_data)
       
      
       
        post_data = {
                'id': thePost.id,
                'post_subject': thePost.subject,
                'post_text': thePost.text,
                'username':thePost.created_by.name,
                'post_category':thePost.category.name,
                'post_subcategory':thePost.sub_category.name,
                'post_images': images,
                'comments':comments,
                'isInMyFavorite':isInMyFavorite
                # Add other fields as needed
            }
        
        print(post_data)
        return JsonResponse(post_data, safe=False)



### http://127.0.0.1:8000/api/locations

def api_locations(request):
    data = list(Location.objects.all().values("id","name"))
    return JsonResponse(data, safe=False)


### http://127.0.0.1:8000/api/categories

def api_categories(request):
    data = list(Post_Category.objects.all().values("id","name"))
    return JsonResponse(data, safe=False)

### http://127.0.0.1:8000/api/subCategory?category='string of category'

def api_subCategoryByCategory(request):
    category = request.GET.get("category")
    postCategory = Post_Category.objects.filter(name=category).first()
    subCategory = list(Sub_Category.objects.filter(category=postCategory).values("id","name"))
    return JsonResponse(subCategory, safe=False)


### http//127.0.0.1:8000/api/addpost
@csrf_exempt
def api_add_post(request):
    if request.method == 'POST':
        post_subject = request.POST.get("post_subject")
        post_text    = request.POST.get("post_text")
        post_category = request.POST.get("post_category")
        post_subcategory = request.POST.get("post_subcategory")
        post_city     = request.POST.get("post_city")
        images = request.FILES.getlist("images")
        username = request.POST.get("username")
        token = request.POST.get("token")

        
        print(f"Server Received request to add new post with the following data:\n"
               f"{username},\n"
               f"{token},\n"
        f"{post_subject},\n"
        f"{post_text},\n"
        f"{post_category},\n"
        f"{post_subcategory},\n"
        f"{post_city}")

        try:
            theUser = User.objects.get(name=username, token=token)
        except ObjectDoesNotExist:
            print("User not found or token not correct")
            return JsonResponse({'status': 'error', 'message': 'User auth error'})
        
        print("the user with token are correct save the post")
        theLocation = Location.objects.filter(name=post_city).first()
        theCategory = Post_Category.objects.filter(name=post_category).first()
        theSub_category = Sub_Category.objects.filter(name=post_subcategory, category=theCategory).first()
        newPost = Post(
                        created_by   = theUser,
                        subject      = post_subject,
                        text         = post_text,
                        location     = theLocation,
                        category     = theCategory,
                        sub_category = theSub_category,
                        
                    )
        newPost.save()
        for image in images:
            postImage = Post_Images(
                                    post  = newPost,
                                    image = image
                                    )
            # Save the image to a file
            postImage.image.save(image.name, image) 
        return JsonResponse({'status': 'success', 'message': 'post added'})
      

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



### http//127.0.0.1:8000/api/add/favorite
@csrf_exempt
def api_add_to_my_favorite(request):
    if request.method =="POST":
        username = request.POST.get("username")
        token    = request.POST.get("token")
        postId   = request.POST.get("postId")
        print(f"add postId {postId} to favorite for user {username} verify token {token}")
        thePost = Post.objects.get(pk=int(postId))
        theUser = User.objects.get(name=username)
        if theUser.token == token:
            print("user token correct so add this post to his favorite")
            ## if post already in my favorite deleted if not add
            isInMyFavorite = MyFavorite.objects.filter(post = thePost, user = theUser).exists()
            if isInMyFavorite:
                myFavoritePost = MyFavorite.objects.filter(post=thePost,user=theUser).first()
                myFavoritePost.delete()
                return JsonResponse({'status': 'post removed from your favorite successfully'})
            else:
                myFavorite = MyFavorite(
                                        user = theUser,
                                        post = thePost
                                    )
                myFavorite.save()
                return JsonResponse({'status': 'post added to your favorite successfully'})
        else:
            return JsonResponse({'status': 'Token problem try to relogin'})
    return JsonResponse({'status': 'only http post request !'})

        




### http//127.0.0.1:8000/api/login
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        username = str(request.POST['username']).lower().replace(" ", "")
        password = request.POST['password']
        print(f'the username value ===>{username}, with password {password}')

        if username.isdigit():
            print(f'user enter his mobile {username}')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    print('user is authenticate')
                    login(request, user)
                    token = get_random_string(length=64)
                    user.token = token
                    user.save()
                    return JsonResponse({'status': 'success', 
                                         'username':user.name,
                                         'message': 'user is authenticate by mobile',
                                         'token':token})
            else:
                # Authentication failed
                print('Authentication failed with mobile')
                error_message = 'أسم المستخدم أو كلمة المرور خطأ'
                return JsonResponse({'status': 'error', 'message': 'username or password incorrect!'})       
        else:
            print(f'the user name {username} want to login with name instead of mobile'  )
          
            userMobile = User.objects.filter(name=username).first()
            if userMobile is None:
                return JsonResponse({'status': 'error', 'message': 'username not exist !'})
                
            user = authenticate(request, username=userMobile.mobile, password=password)
            if user is not None:
                    login(request, user)
                    token = get_random_string(length=64)
                    user.token = token
                    user.save()
                    return JsonResponse({'status': 'success', 
                                         'username':user.name,
                                         'message': 'user is authenticate by username as name',
                                         'token':token})
            else:
                # Authentication failed
                
                print('Authentication failed with name')
                
                return JsonResponse({'status': 'error', 'message': 'Authentication failed with name'})   
    else:
         return JsonResponse({'status': 'error', 'message': 'only http post request'})  



        
       