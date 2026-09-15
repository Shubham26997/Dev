from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializer import UserSerializer, LoginSerializer, UserCreateSerializer

AUTH_TOKEN_TTL = settings.AUTH_TOKEN_TTL
AUTH_TOKEN_KEY = settings.AUTH_TOKEN_KEY

# Create your views here.
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ["login", "register"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "register":
            return UserCreateSerializer
        return super().get_serializer_class()

    def login(self, request):
        req_data = request.data

        serailzer_data = LoginSerializer(data=req_data)
        if not serailzer_data.is_valid():
            return Response(
                {
                    "data": {},
                    "message": serailzer_data.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
        user_data = serailzer_data.validated_data # this will return the complete data including the one with write_only fields
        user_obj = authenticate(email=user_data.get('username'), password=user_data.get('password'))
        if not user_obj:
            return Response(
                {
                    "data": {},
                    "message": "Invalid User Credential"
                }, status=status.HTTP_401_UNAUTHORIZED
            )
        # print(user_obj)
        # Get token from redis cache
        token = cache.get(key=AUTH_TOKEN_KEY.format(user_obj.id), default=None)
        if not token:
            print("Not found in redis DB hit")
            token, _ = Token.objects.get_or_create(user=user_obj)
            token = token.key
            cache.set(AUTH_TOKEN_KEY.format(user_obj.id), value=token, timeout=AUTH_TOKEN_TTL)
        else:
            print("Cache hit found token")

        return Response(
            {
                "data": {
                    "token": token,
                    "user": self.get_serializer(user_obj).data
                },
                "message": "Login Success"
            }, status=status.HTTP_200_OK
        )
    

    def register(self, request):
        req_data = request.data
        serializer_data = self.get_serializer(data=req_data)
        if serializer_data.is_valid():
            self.perform_create(serializer=serializer_data)
            # serializer_data.save()
            return Response(
                {
                    "data": serializer_data.data,
                    "message": "User created successfully"
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "data": [],
                "message": serializer_data.errors   
            }, status=status.HTTP_400_BAD_REQUEST
        )
    
class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    def logout(self, request):
        # Remove the user token from cache and db token
        cache.delete(key=AUTH_TOKEN_KEY.format(request.user.id))
        Token.objects.filter(user = request.user).delete()
        return Response(
            {
                "data": [],
                "message": "Logout Success"
            }, status=status.HTTP_200_OK
        )