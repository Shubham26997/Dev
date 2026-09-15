import re
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    # body = "Hello Welcome to Django <br>\
    # <a href = http://127.0.0.1:8000/removepunc> Remove Punc Char </a><br>\
    # <a href = http://127.0.0.1:8000/titlechar> Capital Char </a><br>\
    # <a href = http://127.0.0.1:8000/newlineremove> Remove New Line </a><br>\
    # <a href = http://127.0.0.1:8000/spaceremove> Remove Space </a><br>\
    # <a href = http://127.0.0.1:8000/charcount> Get Char count </a><br>"
    # return HttpResponse(body)
    return render(request, 'index.html')

def removepunc(request):
    home = "<a href= http://127.0.0.1:8000> Go to Home </a>"
    return HttpResponse(f"Hello Welcome to Django!! Please remove punc char {home}")

def capitalize(request):
    home = "<a href= http://127.0.0.1:8000> Go to Home </a>"
    return HttpResponse(f"Hello Welcome to Django!! Please capital {home}")

def newlineremove(request):
    home = "<a href= http://127.0.0.1:8000> Go to Home </a>"
    return HttpResponse(f"Hello Welcome to Django!! Please newlineremove {home}")

def spaceremove(request):
    input_text = request.GET.get('text', '')
    space_check = request.GET.get('spaceremove', 'off')
    modified_text = input_text
    if space_check == 'on':
        modified_text = re.sub("/s{2,}", ' ', input_text) # this will check for occurance of space for two or more times using /s for space and {2,} for two or more occurance part
    home = "<a href= http://127.0.0.1:8000> Go to Home </a>"
    return HttpResponse(f"Hello Welcome to Django!! Space removed with {modified_text} if wish to retry click {home}")

def charcount(request):
    char_count = len(request.GET.get('text', ''))
    home = "<a href= http://127.0.0.1:8000> Go to Home </a>"
    return HttpResponse(f"Hello Welcome to Django!! The char count is {char_count} if wish to retry click {home}")