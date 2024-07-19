from rest_framework import viewsets,status
from ..models import Task,SubTask
from ..serializers import TaskSerializer,SubTaskSerializer
from django.db import connection
from pprint import pprint

    
class TaskViewset(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related('subtask_task').order_by('id')
    serializer_class = TaskSerializer
    
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)        
        pprint(connection.queries)
        print(len(connection.queries))
        return data
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class SubTaskViewset(viewsets.ModelViewSet):
    queryset = SubTask.objects.all()
    # queryset = SubTask.objects.select_related('parent_task').all()
    serializer_class = SubTaskSerializer
    def list(self, request, *args, **kwargs):
        data = super().list(request, *args, **kwargs)        
        pprint(connection.queries)
        print(len(connection.queries))
        return data