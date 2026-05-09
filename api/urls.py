from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, 
    TaskViewSet, 
    UserViewSet,
    CommentViewSet,
    SubtaskViewSet,
    NotificationViewSet,
    ActivityLogViewSet,
    register_user, 
    login_user, 
    dashboard_stats
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'activity', ActivityLogViewSet, basename='activity')

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('dashboard/', dashboard_stats, name='dashboard'),
    path('', include(router.urls)),
]
