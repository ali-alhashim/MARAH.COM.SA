from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.

### http://127.0.0.1:8000/api/home
def api_home(request):
    return JsonResponse()