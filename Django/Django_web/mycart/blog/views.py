from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

# Create your views here.

def index(request):
    body = """
    Welcome to blog page <br>
        Please select any of the below post for view<br>
        <a href = /blog/1>1</a><br>
        <a href = /blog/2>2</a><br>
        <a href = /blog/3>3</a>"""
    return HttpResponse(body)

def post_id(request, post_id):
    posts = [
        {'id': 1, 'title': "POST 1", 'content': "Post number 1"},
        {'id': 2, 'title': "POST 2", 'content': "Post number 2"},
        {'id': 3, 'title': "POST 3", 'content': "Post number 3"},
    ]
    if post_id > len(posts):
        # return HttpResponseBadRequest()
        return HttpResponseNotFound()
    return render(request, "blog/index.html", context={
        'name': "Shubham Goel",
        'post_req': posts[post_id-1].get('content'),
        'posts': posts
        }
    )
