from django.urls import path
from posts.views import post_list, post_page

urlpatterns = [
    path('list/', post_list, name='post_list'),
    path('<slug:slug>', post_page, name='post_page'),
]