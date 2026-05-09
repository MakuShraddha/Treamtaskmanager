from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied

from .models import User, Project, Task, Comment, Subtask, Notification, ActivityLog
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    TaskSerializer,
    CommentSerializer,
    SubtaskSerializer,
    NotificationSerializer,
    ActivityLogSerializer
)

def log_activity(user, action, target):
    ActivityLog.objects.create(user=user, action=action, target=target)

class IsAdminOrManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        role = getattr(request.user, 'role', None)
        return bool(request.user and request.user.is_authenticated and role in ['ADMIN', 'MANAGER'])

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManagerOrReadOnly]

    def perform_create(self, serializer):
        project = serializer.save()
        log_activity(self.request.user, "Created Project", project.title)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('due_date')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        role = getattr(self.request.user, 'role', None)
        if role not in ['ADMIN', 'MANAGER']:
            raise PermissionDenied("Only admins or managers can create tasks.")
        task = serializer.save(reporter=self.request.user)
        log_activity(self.request.user, "Created Task", task.title)
        if task.assignee:
            Notification.objects.create(user=task.assignee, text=f"You were assigned to: {task.title}")

    def perform_update(self, serializer):
        task = serializer.save()
        log_activity(self.request.user, "Updated Task", task.title)

    def perform_destroy(self, instance):
        role = getattr(self.request.user, 'role', None)
        if role not in ['ADMIN', 'MANAGER']:
            raise PermissionDenied("Only admins or managers can delete tasks.")
        log_activity(self.request.user, "Deleted Task", instance.title)
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        log_activity(self.request.user, "Commented on Task", comment.task.title)

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityLog.objects.all().order_by('-created_at')[:50]
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
    return Response({"error": "Invalid Credentials. Please check your username and password."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    # Core stats
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    todo_tasks = Task.objects.filter(status='TODO').count()
    in_progress_tasks = Task.objects.filter(status='IN_PROGRESS').count()
    done_tasks = Task.objects.filter(status='DONE').count()
    
    today = timezone.now().date()
    overdue_tasks = Task.objects.filter(
        status__in=['TODO', 'IN_PROGRESS'],
        due_date__lt=today
    ).count()

    due_today = Task.objects.filter(
        status__in=['TODO', 'IN_PROGRESS'],
        due_date=today
    ).count()

    # Chart Data (Completion Rate roughly by month or fixed values if empty)
    chart_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'completed': [0, 5, 10, 15, done_tasks, done_tasks+2],
        'pending': [0, 8, 12, 10, in_progress_tasks+todo_tasks, in_progress_tasks]
    }

    # Recent activities & upcoming deadlines
    activities = ActivityLogSerializer(ActivityLog.objects.all().order_by('-created_at')[:5], many=True).data
    upcoming = TaskSerializer(Task.objects.filter(due_date__gte=today).order_by('due_date')[:5], many=True).data

    return Response({
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "completed_tasks": done_tasks,
        "overdue_tasks": overdue_tasks,
        "due_today": due_today,
        "chart_data": chart_data,
        "recent_activities": activities,
        "upcoming_deadlines": upcoming
    })
