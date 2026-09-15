from django.urls import path
from note.views import NoteViewSet, home_note
app_name = "notes"
urlpatterns = [
    path('', home_note, name="home_note"),
    path('note/', NoteViewSet.as_view({"get": "list_note", "post":"create_note"}), name="note_list"),
    path('note/<int:pk>/', NoteViewSet.as_view({"put":"edit_note", "delete": "delete_note"}), name="note_update")
]