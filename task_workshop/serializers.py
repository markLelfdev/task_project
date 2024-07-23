from django.utils import timezone
from rest_framework import serializers
from task_workshop.models import SubTask, Task
from django.contrib.auth.models import User
from collections import OrderedDict


class UserUpdatedSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects, required=False)
    updated_by = serializers.PrimaryKeyRelatedField(queryset=User.objects, required=False)

    def update(self, instance, validated_data):
        validated_data.update({"updated_by": self._context["request"].user})
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        validated_data.update({
            "created_by": self._context["request"].user,
            "updated_by": self._context["request"].user,
        })
        return super().create(validated_data)

class SubTaskSerializer(UserUpdatedSerializer,serializers.ModelSerializer):
    parent_task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(),required=False)
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
            'updated_at': timezone.now(),
        })
        
        if task_parentid is not None:
            subtask_create = SubTask.objects.create(parent_task=task_parentid, **validated_data)
            
        return subtask_create
        
    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data.update({
            'updated_by': user,
            'updated_at': timezone.now(),
        })
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        assignee_name = instance.assignee.username if instance.assignee != None else None
        resentation = {
            'id': instance.id,
            'title': instance.title,
            'status': instance.get_status_display(),
            'assignee': assignee_name,
            'task' : instance.parent_task.title
        }
        return resentation

class TaskSerializer(UserUpdatedSerializer,serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, required=False)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = Task
        fields = ['id','title','status','assignee','subtasks']
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assignee = validated_data.pop('assignee', [])
        if assignee :
            validated_data.update({'assignee': assignee})
        instance =  super().create(validated_data)
        
        for subtask in subtasks_data :
            subtask.update({
                'parent_task': instance
            })
            SubTaskSerializer(context=self.context).create(validated_data=subtask)
        return instance

    
    # def create(self, validated_data):
    #     subtasks_data = validated_data.pop('subtasks', [])
    #     assignee = validated_data.pop('assignee', [])
    #     if assignee :
    #         validated_data.update({'assignee': assignee})
        
    #     # print(validated_data)
    #     task_create = TaskSerializer(data=validated_data)
    #     task_create.is_valid(raise_exception=True)
    #     task_create.save()
    #     return task_create
    #     # Task.objects.create( **validated_data)
    #     # # create subtask
    #     # if subtasks_data :
    #     #     for subtask_l in subtasks_data:
    #     #         subtask_l.update({
    #     #             'parent_task': task_create,
    #     #             'created_at': timezone.now()
    #     #             })
    #     #         SubTask.objects.create( **subtask_l)
    #     # return task_create

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', None)
        user = self.context['request'].user
        validated_data.update({
            'updated_by': user,
            'updated_at': timezone.now(),
        })
        
        if new_status is not None and new_status != instance.status:
            print(new_status)
            # หา subtask 
            subtask = instance.subtask_task.all()
            for sub in subtask:
                # subtask น้อยกว่า Task
                if sub.status < new_status:
                    print('Change status')
                    print(sub.status,sub.title)
                    sub.status = new_status
                    sub.updated_by = user
                    sub.updated_at = timezone.now()
                    sub.save()
        super().update(instance, validated_data)
        return instance
    
    def to_representation(self, instance):
        assignee_name = instance.assignee.username if instance.assignee != None else None
        subtask_query = instance.subtask_task.select_related('parent_task').all()
        # representation = OrderedDict()
        resentation = {
            'id': instance.id,
            'title': instance.title,
            'status': instance.get_status_display(),
            'assignee': assignee_name,
            'subtask' : SubTaskSerializer(subtask_query,many=True).data
        }
        return resentation
