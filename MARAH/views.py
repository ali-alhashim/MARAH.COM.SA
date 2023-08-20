from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'Marah/home.html',{})




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