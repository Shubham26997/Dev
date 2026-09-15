from django.urls import path
from user.views import UserViewSet, LogoutViewSet
app_name = "users"
urlpatterns = [
    path('login/', UserViewSet.as_view({"post":"login"}), name="user_login"),
    path('logout/', LogoutViewSet.as_view({"get":"logout"}), name="user_logout"),
    path('sign_up/', UserViewSet.as_view({"post":"register"}), name="user_register"),

]