from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import  OuterRef, Subquery
from post_app.models import Post, Location, Post_Images, Post_Category, Sub_Category
from django.contrib.auth import authenticate, login
from user_app.models import User
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
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

### http://127.0.0.1:8000/api/subCategory?category='string of category'

def api_subCategoryByCategory(request):
    category = request.GET.get("category")
    postCategory = Post_Category.objects.filter(name=category).first()
    subCategory = list(Sub_Category.objects.filter(category=postCategory).values("id","name"))
    return JsonResponse(subCategory, safe=False)


### http//127.0.0.1:8000/api/addpost
def api_add_post(request):
    return JsonResponse({'status': 'success', 'message': 'post added'})







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



        
       