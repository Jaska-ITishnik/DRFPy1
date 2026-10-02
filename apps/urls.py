from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import TaskModelViewSet

router = DefaultRouter()
router.register("tasks", TaskModelViewSet, basename="task")
urlpatterns = [
    path("", include(router.urls))
]
