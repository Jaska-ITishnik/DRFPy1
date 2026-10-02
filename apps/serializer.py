from rest_framework.serializers import ModelSerializer

from apps.models import Task


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        # fields = "id", "title", "is_done", "created_at"
        fields = "__all__"
        # exclude = ()
        read_only_fields = "id", "created_at"
