from django.shortcuts import render
from django.http import HttpResponse

from posts.models import Post
# Create your views here.

def post_list(request):
    # posts = Post.objects.all()
    # return HttpResponse(f"Posts list created with {posts.values_list('title')[0]}")
    return render(request, template_name='posts_list.html')
    # return HttpResponse("Posts List created listed here")

def post_page(request, slug):
    post = Post.objects.filter(slug=slug).first()
    return HttpResponse(post)