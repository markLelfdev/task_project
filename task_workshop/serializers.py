from django.utils import timezone
from rest_framework import serializers
from task_workshop.models import SubTask, Task
from django.contrib.auth.models import User



class SubTaskSerializer(serializers.ModelSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),write_only=True)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = SubTask
        fields = ['id','title','status','assignee','parent_task']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        task_parentid = validated_data.pop('parent_task',None)
        # print(task_parentid)
        validated_data.update({
            'created_by': user,
            'updated_by': user,
            # 'assigned': user,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        })
        if task_parentid is not None:
            subtask_create = SubTask.objects.create(parent_task=task_parentid, **validated_data)
        
        return subtask_create
        # return SubTask.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = Task
        fields = ['id','title','status','assignee','subtasks']
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks',[])
        user = self.context['request'].user
        # print('subtasks_data')
        validated_data.update({
            'created_by': user,
            'updated_by': user,
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
        })
        # print(validated_data)
        task_create = Task.objects.create(**validated_data)
        if subtasks_data :
            try:
                for subtask_l in subtasks_data:
                    subtask_l.update({
                        'parent_task': task_create,
                        'created_by': user,
                        'updated_by': user,
                        'created_at': timezone.now(),
                        'updated_at': timezone.now(),
                    })
                    SubTask.objects.create(**subtask_l)
            except Exception as e:
                print(f"Error creating subtasks: {str(e)}")
        return task_create

    def update(self, instance, validated_data):
        # 
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        assignee_name = instance.assignee.username if instance.assignee != None else None
        resentation = {
            'id': instance.id,
            'title': instance.title,
            'status': instance.get_status_display(),
            'assignee': assignee_name,
            'subtask' : SubTaskSerializer(instance.subtask_task.all(),many=True).data
        }
        return resentation
