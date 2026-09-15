from django.urls import path
from blog.views import index, post_id

urlpatterns = [
    path("", view=index, name="BlogHome"),
    path("<int:post_id>", view=post_id, name="BlogPost"),
]