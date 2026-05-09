# Nexus Enterprise Task Manager

A comprehensive Task and Project Management system featuring a Django backend and a responsive HTML/CSS/JavaScript frontend. It includes full CRUD operations for projects, tasks, and users, with role-based access control (RBAC).

## Features
- **Project Management**: Create, read, update, and delete projects.
- **Task Management**: Assign tasks, update status, and track progress.
- **User Management**: Role-based access control for different team members.
- **Responsive UI**: A modern, dynamic frontend built with vanilla web technologies.

## Tech Stack
- **Backend**: Python, Django, Django REST Framework, SQLite
- **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript

## Setup Instructions

### 1. Backend Setup
Make sure you have Python installed on your system.

Open a terminal in the root directory (`taskmanagement`) and run the following commands:

```bash
# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install dependencies (if you haven't already and have a requirements.txt, otherwise the venv should be ready)
# pip install django djangorestframework django-cors-headers

# Apply database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
```

The backend API will be running at `http://127.0.0.1:8000/`.

### 2. Frontend Setup
The frontend consists of static files, so no build step is required. 

To run the frontend, you have a few options:
- **Using a local server (Recommended)**: Use a tool like Live Server (VS Code extension) or Python's built-in HTTP server to serve the `frontend` directory.
  ```bash
  cd frontend
  python -m http.server 5500
  ```
  Then, navigate to `http://127.0.0.1:5500/` in your browser.
- **Direct file access**: You can simply open `frontend/index.html` directly in your web browser.

## API Endpoints
- `/api/projects/` - Manage Projects
- `/api/tasks/` - Manage Tasks
- `/api/users/` - Manage Users

## License
MIT
