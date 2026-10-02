from django.db.models.base import Model
from django.db.models.fields import CharField, BooleanField, DateTimeField


# Create your models here.
class Task(Model):
    title = CharField(max_length=255, verbose_name="Sarlavha")
    is_done = BooleanField(db_default=False)
    created_at = DateTimeField(auto_now_add=True)
