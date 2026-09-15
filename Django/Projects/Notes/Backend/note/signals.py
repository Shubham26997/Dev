from django.dispatch import receiver
from datetime import datetime
from django.db.models.signals import pre_save
from note.models import Note

@receiver(pre_save, sender=Note)
def update_last_update(sender, instance, **kwargs):
    instance.last_updated_date = datetime.now()