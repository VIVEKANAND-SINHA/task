from django.urls import path
from .views import TaskCreateApi,TaskAssignToUsersApi,TaskUserWise

urlpatterns = [
    path('create/', TaskCreateApi.as_view(), name='create-task'),
    path('assign/', TaskAssignToUsersApi.as_view(), name='assign-task'),
    path('get-tasks/<int:user_id>/', TaskUserWise.as_view(), name='task-by-user'),
]
