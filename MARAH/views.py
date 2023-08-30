from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from post_app.models import Post
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from post_app.models import Location, Post_Category

def home(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'Marah/home.html',{"posts":posts})


def search(request):
    print('Start Search View....')
    category  = request.GET.get('category')
    searchKey = request.GET.get('searchKey')
    selectedLocation  = request.GET.get('location')

    query = Q()
    print('location:', selectedLocation)
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
    posts = Post.objects.filter(query).order_by('-created_date')
    return render(request,'Marah/search.html',{"posts":posts,"selectedLocation":selectedLocation,"selectedcategory":category})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired URL
        else:
            # Authentication failed
            error_message = 'Invalid username or password'
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