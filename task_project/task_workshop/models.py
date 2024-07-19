from django.db import models
from django.contrib.auth.models import User
from safedelete.models import SafeDeleteModel,SOFT_DELETE_CASCADE,SafeDeleteManager
# Create your models here.
class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    original_objects = models.Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="%(class)s_created_by",on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, related_name="%(class)s_updated_by",on_delete=models.CASCADE)
    @property
    def log_str(self):
        return f'{self.title}:{self.pk}'

    class Meta:
        abstract = True

class CustomIntegerChoices(models.IntegerChoices):
    # การทำ choice สำหรับการแสดง Json
    @classmethod
    def get_choices_items(cls):
        empty = [(None, cls.__empty__)] if hasattr(cls, "__empty__") else []
        return empty + [{"value": member.value, "label": member.label} for member in cls]
    
class status_type(CustomIntegerChoices):
        Todo = 0,'Todo'
        In_Progress = 1,'In Progress'
        Review = 2,'Review'
        Done = 3,'Done'

class Task(BaseModel):
    id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices=status_type.choices,default=status_type.Todo,null=False,blank=False)
    assignee = models.ForeignKey(User, related_name="%(class)s_user_assign",on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.title

class SubTask(BaseModel):
    id = models.AutoField(primary_key=True,auto_created=True)
    title = models.CharField(max_length=100)
    status = models.IntegerField(choices=status_type.choices,default=status_type.Todo,null=False,blank=False)
    assignee = models.ForeignKey(User, related_name="%(class)s_user_assign",on_delete=models.CASCADE, null=True)
    parent_task = models.ForeignKey(Task, related_name="%(class)s_task",on_delete=models.CASCADE)
    def __str__(self):
        return self.title