from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login(request):
    # return HttpResponse("Login Page")
    return render(request, template_name="users_login.html")

def sign_up(request):
    # return HttpResponse("Sign Up Page")
    return render(request, template_name='sign_up.html')