from .models import Task

def task_by_user(user):
    """
    Retrieves tasks assigned to a specific user based on user_id.

    Parameters:
        user: Instance of user model

    Returns:
        queryset: Containing task details.

    Raises:
        DatabaseError: If there is an issue fetching data from the database.
    """
    try:
        tasks = Task.objects.filter(assigned_user=user)
        return tasks
    except Exception as e:
        return {"error": str(e)}
