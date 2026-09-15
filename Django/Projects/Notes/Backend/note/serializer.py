from rest_framework import serializers
from note.models import Note
from user.serializer import UserSerializer

class NoteSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Note
        fields = ("id", "title", "content", "created_date", "is_completed", "author")

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty or just whitespace.")
        queryset = Note.objects.filter(title__iexact=value.strip(), is_active=True)
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id) # Exclude the current instance when updating
        if queryset.exists():
            raise serializers.ValidationError("A note with this title already exists.")
        return value.strip()
    
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content can't be Empty, Please add some valid data")
        return value.strip()