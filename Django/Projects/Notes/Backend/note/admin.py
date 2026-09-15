from django.contrib import admin
from note.models import Note
# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    def striped_content(self, obj):
        return obj.content[:10]+"..."
    ordering = ["-created_date"]
    list_display = ["id", "title", "created_date",
                    "is_completed", "striped_content"]
    # list_filter = ("authour",)
    search_fields = ("title",)
    striped_content.short_description = "content preview"