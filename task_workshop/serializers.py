from django.utils import timezone
from rest_framework import serializers
from task_workshop.models import SubTask, Task
from django.contrib.auth.models import User
from collections import OrderedDict
import task_workshop.util as util


class SubTaskSerializer(serializers.ModelSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.prefetch_related('subtask_task'),required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = SubTask
        fields = ['id','title','status','assignee','parent_task']
    
    def create(self, validated_data):
        user = self.context['request'].user
        task_parentid = validated_data.pop('parent_task', None)
        assignee = validated_data.pop('assignee', [])
        if assignee :
            validated_data.update({'assignee': assignee})
            
        validated_data.update({
            'created_by': user,
            'updated_by': user,
            'created_at': timezone.now(),
        })
        
        if task_parentid is not None:
            subtask_create = SubTask.objects.create(parent_task=task_parentid, **validated_data)
            
        return subtask_create
        
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data.update({
            'updated_by': user,
        })
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        assignee_name = instance.assignee.username if instance.assignee != None else None
        resentation = {
            'id': instance.id,
            'title': instance.title,
            'status': instance.get_status_display(),
            'assignee': assignee_name,
            'updated': util.localize_time(instance.updated_at),
            'task' : instance.parent_task.title
        }
        return resentation


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                                                  allow_null=True, 
                                                  required=False,
                                                  error_messages={'does_not_exist': 'User not found in systems',})
    
    class Meta:
        model = Task
        fields = ['id','title','status','assignee','updated_by','subtasks']
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        user = self.context['request'].user
        assignee = validated_data.pop('assignee', [])
        if assignee :
            validated_data.update({'assignee': assignee})
        validated_data.update({
            'created_by': user,
            'updated_by': user,
            'created_at': timezone.now(),
        })
        # print(validated_data)
        task_create = Task.objects.create( **validated_data)
        # create subtask
        if subtasks_data :
            for subtask_l in subtasks_data:
                subtask_l.update({
                    'parent_task': task_create,
                    'created_by': user,
                    'updated_by': user,
                    'created_at': timezone.now()
                    })
                SubTask.objects.create( **subtask_l)
        return task_create

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', None)
        user = self.context['request'].user
        
        validated_data.update({
            'updated_by': user,
        })
        
        if new_status is not None and new_status != instance.status:
            # print(new_status)
            subtask = instance.subtask_task.all()
            self.update_task(subtask, new_status,user)
        super().update(instance, validated_data)
        return instance
    
    # def update subtask all
    def update_task(self,task, new_status, user):
        for subtask in task:
            if subtask.status < new_status :
                subtask.status = new_status
                subtask.updated_by = user
                subtask.save()
    
    def to_representation(self, instance):
        assignee_name = instance.assignee.username if instance.assignee != None else None
        subtask_query = instance.subtask_task.select_related('parent_task').all()
        # representation = OrderedDict()
        resentation = {
            'id': instance.id,
            'title': instance.title,
            'status': instance.get_status_display(),
            'updated':  util.localize_time(instance.updated_at),
            'assignee': assignee_name,
            'subtask' : SubTaskSerializer(subtask_query,many=True).data
        }
        return resentation

