from django.urls import path
from users.views import login, sign_up

urlpatterns = [
    path('login/', login, name='login_page'),
    path('register/', sign_up, name='sign_up_page'),
]