from rest_framework.exceptions import ValidationError, NotFound
from tasks.models import Task, User
from django.db import  transaction

def task_create(data):
    """
    Creates a new task.

    Parameters:
        data (dict): Dictionary containing task details.
            - name (str): Name of the task.
            - description (str): Description of the task.

    Returns:
        dict: Success message and task details if created successfully.
    
    Raises:
        ValidationError: If required fields are missing or creation fails.
    """
    try:
        name = data.get('name')
        description = data.get('description')

        if not name or not description:
            raise ValidationError(detail="Task 'name' and 'description' are required.")

        task = Task.objects.create(
            name=name,
            description=description
        )

        return {
            "message": "Task created successfully.",
            "task_id": task.id,
            "name": task.name,
            "description": task.description
        }

    except ValidationError as ve:
        raise ve
    except Exception as e:
        raise ValidationError(detail=f"Failed to create task: {str(e)}")


def task_assign_to_users(data):
    """
    Assigns a task to multiple users.

    Parameters:
        data (dict): Dictionary containing user and task details.
            - user_ids (list): List of user IDs to assign the task.
            - task_id (int): ID of the task to be assigned.

    Returns:
        dict: A success message along with assigned  already assigned and user not founded users.

    Raises:
        NotFound: If the task is not found.
        ValidationError: If input data is invalid.
    """
    try:
        user_ids = data.get('user_ids', [])
        task_id = data.get('task_id')


        if not isinstance(user_ids, list) or not task_id:
            raise ValidationError(detail="Invalid input: 'user_ids' must be a list and 'task_id' is required.")

        # Fetch task
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail=f"Task with ID {task_id} not found.")

        assigned_users = []
        already_assigned_users = []
        user_not_found = []

        

        with transaction.atomic():
            for user_id in user_ids:
                user = User.objects.filter(id=user_id).first()
                if not user:
                    user_not_found.append(user_id)
                    continue

                if task.assigned_user.filter(id=user.id).exists():
                    already_assigned_users.append(user.id)
                else:
                    task.assigned_user.add(user)
                    assigned_users.append(user.id)

            task.save()

        return {
            "message": "Users assigned successfully.",
            "assigned_users": assigned_users,
            "already_assigned_users": already_assigned_users,
            "users_not_found":user_not_found,
            "task_id": task_id
        }

    except NotFound as nf:
        raise nf
    except ValidationError as ve:
        raise ve
    except Exception as e:
        
        raise ValidationError(detail=f"Failed to assign users: {str(e)}")
