from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.task import TaskViewset,SubTaskViewset


router = DefaultRouter()
# router.register(r'classrooms', ClassroomViewSet)

router.register(r'tasks', TaskViewset,basename='tasks')
router.register(r'subtasks', SubTaskViewset,basename='subtasks')
api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls)),
]

