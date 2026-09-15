from django.contrib import admin
from posts.models import Post, Tag
# Register your models here.

# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=("title", "slug")
    list_filter = ["slug"]
    search_fields = ["title"]
    ordering = ["-date"]
    # date_hierarchy = "date" # just adding dates filter at the top of records listing which is not in previous records
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name',)