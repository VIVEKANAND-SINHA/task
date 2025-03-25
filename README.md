# Task Management API

This is a Django-based Task Management API that allows users to create, assign, and get tasks for a particular user.

## 🚀 Features

- Task creation, assignment, and user wiser assigned tasks.
- Pagination
- Admin panel for managing users and tasks.
- Lightweight API responses optimized for performance.

---

## 📌 Prerequisites

Make sure you have the following installed:

- **Python** (>=3.8)
- **pip** (Python package manager)
- **Virtualenv** (recommended)

---

## ⚙️ Setup Instructions

1. **Clone the repository**

   ```sh
   git clone https://github.com/VIVEKANAND-SINHA/task.git
   cd task_manager
   ```

2. **Create a virtual environment**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access)**

   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```sh
   python manage.py runserver or python manage.py runserver [port]
   ```

---

## API Endpoints

### 🔹 Task Management

- **Create a Task**: `POST api/v1/task/create/`
- **Assign Task to User**: `PUT api/v1/task/assign/`
- **Get Tasks by User**: `GET /api/v1/task/get-tasks/<int:user_id>/`

\*\*/admin/ - for admin panel

### 🔹 Sample API Request

#### Create a Task (`POST /api/v1/task/create/`)

```json
{
  "name": "Create a Readme file",
  "description": "A readme file to describe about the project"
}
```

### 🔹 Sample API Response

```json
{
  "success": true,
  "data": {
    "id": 7,
    "assigned_user": [],
    "name": "Create a Readme file",
    "description": "A readme file to describe about the project",
    "created_at": "2025-03-25T18:36:26.416600Z",
    "completed_at": null,
    "task_type": "task",
    "status": "pending"
  }
}
```

#### Assign a Task (`PUT api/v1/task/assign/`)

##### Request

```json
{
  "task_id": 7,
  "user_ids": [1, 2, 5, 3]
}
```

##### Response

```json
{
  "message": "Users assigned successfully.",
  "assigned_users": [1, 2, 3],
  "already_assigned_users": [],
  "users_not_found": [5],
  "task_id": 7
}
```

#### Get Tasks of a user (`GET /api/v1/task/get-tasks/<int:user_id>/`)

##### Response

```json
{
    "limit": 1, ( here limit is set to 1 to check for the next and prev links)
    "offset": 0,
    "count": 2,
    "next": "http://127.0.0.1:8000/api/v1/task/get-tasks/1/?limit=1&offset=1",
    "previous": null,
    "results": [
        {
            "id": 7,
            "name": "Create a Readme file",
            "description": "A readme file to describe about the project",
            "created_at": "2025-03-25T18:36:26.416600Z",
            "completed_at": null,
            "task_type": "task",
            "status": "pending",
            "assigned_user": [
                1,
                2,
                3
            ]
        }
    ]
}
```

---

## 🛠 Admin Panel

- Access the admin panel at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- Log in with the superuser credentials.

---

## 👩‍💻 Author

Developed by **Vivekanand Sinha**
