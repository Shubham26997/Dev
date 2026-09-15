from rest_framework import serializers
from user.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("phone_number",)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    admin = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = User
        fields = ("email", "name", "admin", "password")

    def create(self, validate_data):
        admin = validate_data.pop("admin", None)
        password = validate_data.pop("password")

        user_obj = User(**validate_data)
        user_obj.set_password(password)

        if admin:
            user_obj.is_staff=True
            user_obj.is_superuser=True
        user_obj.save()
        return user_obj

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("email", "name", "profile")

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
