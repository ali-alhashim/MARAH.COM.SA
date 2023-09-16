from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from post_app.models import Post
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from post_app.models import Location, Post_Category, Sub_Category, Post_Comment, Post_Images
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Subquery, OuterRef
from django.db.models import Count
from django.db.models.functions import Coalesce
from user_app.models import User
import math
from django.contrib import messages

def home(request):

   
    items_per_page = 10
    posts = Post.objects.all().order_by('-created_date')
    paginator = Paginator(posts, items_per_page)
    page = paginator.get_page(1)
    print('home page_number =>', 1)

    return render(request, 'Marah/home.html',{"posts":page})


##---------------------------------- Search ---------------------------------------------------

def search(request):
    print('Start Search View....')
    category  = request.GET.get('category')
   
    searchKey = request.GET.get('searchKey')
    selectedLocation  = request.GET.get('location')
    page_number = request.GET.get('page_number',1)
    

    query = Q()
    print('location:', selectedLocation)


    if  request.GET.get('SubCategory') =='all':
        selectedSubCategory = 'all'
    elif request.GET.get('SubCategory') is not None:
         selectedSubCategory = request.GET.get('SubCategory')
         sub_categoryObj = Sub_Category.objects.get(pk=selectedSubCategory)
         query &= Q(sub_category = sub_categoryObj)
    else:
        selectedSubCategory = 'all'

    if selectedLocation != 'all':
       
        locationObj = Location.objects.get(pk=selectedLocation)
        print('you select location ', locationObj.name)
        query = Q(location = locationObj)
        selectedLocation = locationObj
    if category !='all':
        categoryObj = Post_Category.objects.get(pk=category)
        category = categoryObj
        query &= Q(category = categoryObj)

    print('your query = ', query)

    items_per_page = 10

    posts     = Post.objects.filter(query, Q(subject__icontains = searchKey) | Q(text__icontains = searchKey)).order_by('-created_date')
    paginator = Paginator(posts, items_per_page)
    page      = paginator.get_page(page_number)
    return render(request,'Marah/search.html',{"posts":page,"selectedLocation":selectedLocation,"selectedcategory":category,"selectedSubCategory":selectedSubCategory,"page_number":page_number})

## ---------------------------------------------------- search --------------------------------------------------------------------------


def login_view(request):
    if request.method == 'POST':
        username = str(request.POST['username']).lower().replace(" ", "")
        print(f'the username value ===>{username}')
        password = request.POST['password']

        if username.isdigit():
            print(f'user enter his mobile {username}')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                    print('user is authenticate')
                    login(request, user)
                    return redirect('home')
            else:
                # Authentication failed
                print('Authentication failed with mobile')
                error_message = 'أسم المستخدم أو كلمة المرور خطأ'
                return render(request, 'Marah/login.html', {'error_message': error_message})       
        else:
            print(f'the user name {username} want to login with name instead of mobile'  )
            userMobile = User.objects.filter(name=username).first()
            user = authenticate(request, username=userMobile.mobile, password=password)
            if user is not None:
                    login(request, user)
                    return redirect('home')
            else:
                # Authentication failed
                
                print('Authentication failed with name')
                error_message = 'أسم المستخدم أو كلمة المرور خطأ'
                return render(request, 'Marah/login.html', {'error_message': error_message})       
        
       

      

    return render(request, 'Marah/login.html')





### Logout
class LogoutInterfaceView(LogoutView):
    template_name = 'Marah/logout.html'
    def get(self, request, *args, **kwargs):
      
        context = self.get_context_data(**kwargs)
        logout(self.request)

        return self.render_to_response(context)
    



def custom_error_403(request, exception):
    return render(request, '',{})







def load_more_posts(request):
    page_number = request.GET.get('page_number')
    print('load more page #', page_number)
    items_per_page = 10

    comment_count_subquery = Post_Comment.objects.filter(post=OuterRef('id')).values('post').annotate(comment_count=Coalesce(Count('id'), 0)).values('comment_count')
    
    image_subquery = Post_Images.objects.filter(post=OuterRef('id')).order_by('id').values('image')[:1]
    

    posts = Post.objects.all().order_by('-created_date').annotate(comment_count=Subquery(comment_count_subquery), first_image=Subquery(image_subquery)).values('id', 'subject', 'category__name', 'sub_category__name', 'location__name', 'created_date', 'created_by__nikname', 'comment_count', 'first_image')
    paginator = Paginator(posts, items_per_page)

    print("get page #", page_number)
    page = paginator.get_page(page_number)

    Totalposts = Post.objects.all().count()
   
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
