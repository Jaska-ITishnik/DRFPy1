from django.contrib.auth.models import User
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, BooleanField, DateTimeField
from django.db.models.fields.related import ForeignKey


# Create your models here.
class Task(Model):
    owner = ForeignKey(User, on_delete=CASCADE, null=True)
    title = CharField(max_length=255, verbose_name="Sarlavha")
    is_done = BooleanField(db_default=False)
    created_at = DateTimeField(auto_now_add=True)
