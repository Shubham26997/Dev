from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User, Profile
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["-id"]
    list_display = ('id','email', 'name', 'is_staff')
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2"),
        }),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user__name', 'user__email', 'phone_number']
    search_fields = ('user__name', 'user__email')
    list_filter = ('user__email',)

