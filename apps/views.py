from rest_framework.viewsets import ModelViewSet

from apps.models import Task
from apps.serializer import TaskModelSerializer


# Create your views here.
class TaskModelViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
