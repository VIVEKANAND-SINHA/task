from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.pagination import LimitOffsetPagination, get_paginated_response
# from rest_framework.pagination import LimitOffsetPagination

from tasks.services import task_create, task_assign_to_users
from tasks.selectors import task_by_user
from .serializers import TaskSerializer,TaskSerializerUserWise
from .models import User
import logging

# Initialize Logger
logger = logging.getLogger(__name__)


class TaskCreateApi(APIView):
    """
    API endpoint to create a new task.

    Methods:
        - POST: Creates a new task with the given data.

    Request Body:
        - name (str): The name of the task.
        - description (str): A brief description of the task.

    Responses:
        - 201 Created: Task created successfully.
        - 400 Bad Request: Invalid request data.
    """

    def post(self, request):
        try:
            task = task_create(request.data)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Task creation failed: {str(e)}")
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class TaskAssignToUsersApi(APIView):
    """
    API endpoint to assign a task to multiple users.

    Methods:
        - PUT: Assigns a task to the specified users.

    Request Body:
        - task_id (int): The ID of the task to be assigned.
        - user_ids (list[int]): List of user IDs to assign the task.

    Responses:
        - 200 OK: Task assigned successfully.
        - 400 Bad Request: Invalid request data.
    """

    def put(self, request):
        try:
            task_update = task_assign_to_users(request.data)
            return Response(task_update, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Task assignment failed: {str(e)}")
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)


class TaskUserWise(APIView):
    """
    API endpoint to retrieve tasks assigned to a specific user.

    URL Parameters:
        - user_id (int): The ID of the user whose tasks need to be retrieved.

    Responses:
        - 200 OK: Returns a paginated list of tasks assigned to the user.
        - 400 Bad Request: User not found.
        - 500 Internal Server Error: Unexpected error.
    """

    class Pagination(LimitOffsetPagination):
        default_limit = 1

    def get(self, request, user_id):
        try:
            # Fetch user
            user = User.objects.filter(id=user_id).first()

            # If user does not exist, return an error response
            if not user:
                return Response({"error": "User not found with the given user ID"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch tasks assigned to the user
            tasks = task_by_user(user)

            return get_paginated_response(
                pagination_class=self.Pagination,
                serializer_class=TaskSerializerUserWise,
                queryset=tasks,
                request=request,
                view=self
            )

        except Exception as e:
            logger.error(f"Error fetching tasks for user {user_id}: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
