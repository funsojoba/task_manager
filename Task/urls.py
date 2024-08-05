from django.urls import path
from .views import TaskViewSet, TaskDetailAPIView


urlpatterns = [
    path("", TaskViewSet.as_view(), name="tasks"),
    path("<str:pk>", TaskDetailAPIView.as_view(), name="task_detail")
]