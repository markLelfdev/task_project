from rest_framework import viewsets,status
from ..models import Task,SubTask
from ..serializers import TaskSerializer,SubTaskSerializer
    
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class SubTaskViewset(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer