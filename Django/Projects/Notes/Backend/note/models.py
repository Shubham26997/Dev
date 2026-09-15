from django.db import models
from user.models import User

# Create your models here.
class Note(models.Model):
    title = models.CharField("Title of Note", max_length=50)
    content = models.TextField("Notes Content")
    created_date = models.DateTimeField("Created Date", auto_now_add=True)
    last_updated_date = models.DateTimeField("Last Updated", null=True, blank=True)
    is_active = models.BooleanField("Is Active", default=True)
    is_completed = models.BooleanField("Task Done", default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    def __str__(self):
        return self.title