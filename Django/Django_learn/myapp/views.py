# from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    # return HttpResponse("I am home, Welcome to my world")
    return render(request, 'home.html')

def about(request):
    # return HttpResponse("My about section")
    return render(request, 'about.html')