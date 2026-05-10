# ⚡ Nexus Enterprise | Team Task Manager

A comprehensive, enterprise-grade Task and Project Management system featuring a robust Django backend and a stunning, responsive HTML/CSS/JavaScript frontend. Nexus Enterprise delivers a premium user experience with dark mode themes, drag-and-drop Kanban boards, and role-based access control (RBAC).

## ✨ Features

- **Dynamic Kanban Board**: Drag-and-drop tasks across To Do, In Progress, and Done.
- **Project Portfolios**: Create, edit, and delete detailed project outlines with deadlines and assigned teams.
- **Analytics & Reports**: Visual charts tracking employee productivity and task completion rates using Chart.js.
- **Full Calendar View**: Interactive calendar integrating all task deadlines.
- **Role-Based Access Control (RBAC)**: Secure separation between Admins, Managers, and Employees.
- **Admin Verification Workflow**: New user signups remain inactive until an Admin explicitly grants them access via the dedicated Team Management dashboard.
- **Rich Task Details**: Subtasks, comment threads, tags, and file attachments.
- **Premium UI**: Glassmorphism elements, dynamic micro-animations, and a responsive layout designed for both desktop and mobile.

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework, SQLite (Configurable for PostgreSQL)
- **Frontend**: HTML5, Vanilla CSS, Vanilla JS, Chart.js, FullCalendar, SortableJS
- **Production**: Gunicorn, Whitenoise (Static Files)

---

## 🚀 Local Setup Instructions

Nexus serves both the API and the Frontend seamlessly from a single Django instance.

### 1. Prerequisites
Make sure you have Python installed on your system.

### 2. Installation
Open a terminal in the root directory (`taskmanagement`) and run the following commands:

```bash
# Activate the virtual environment (Windows)
venv\Scripts\activate

# Install all necessary dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Start the Django development server
python manage.py runserver
```

### 3. Usage
- Open your browser and navigate to `http://127.0.0.1:8000/`.
- **Note on Registration**: The very first user to register on a fresh database is automatically approved and granted `ADMIN` privileges. Any subsequent registrations will require this Admin to log in and approve the new accounts via the **Team Management** tab.

---

## ☁️ Deployment (Railway)

This application is completely configured to be deployed automatically to [Railway.app](https://railway.app/).

1. **Commit and Push**: Ensure all files (including `requirements.txt` and `Procfile`) are pushed to your GitHub repository.
2. **Deploy**: Go to Railway, click **New Project**, and select **Deploy from GitHub repo**.
3. **Environment Variables**: In your Railway project settings, it is highly recommended to add the following variables:
   - `DEBUG`: Set to `False` for production security.
   - `SECRET_KEY`: Provide a secure, unique Django secret key.
4. **Volumes (SQLite Only)**: If you are relying on the default SQLite database, you MUST attach a Volume to your Railway deployment mounted at `/app` to prevent data loss when the server restarts. Alternatively, spin up a PostgreSQL database in Railway and update `settings.py` accordingly.

---

## 🔗 API Endpoints

- `/api/projects/` - Full CRUD on Projects
- `/api/tasks/` - Full CRUD on Tasks
- `/api/subtasks/` - Subtask checklists
- `/api/comments/` - Task discussion threads
- `/api/users/` - User Management (Admin specific functions available)
- `/api/dashboard/` - Analytical aggregation for charts
- `/api/notifications/` - User notifications

## 📄 License
MIT License
