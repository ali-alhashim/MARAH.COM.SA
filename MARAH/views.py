from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from post_app.models import Post
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
def home(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'Marah/home.html',{"posts":posts})




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