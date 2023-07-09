from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import permissions

from .models import Course

User = get_user_model()


class CreateOrDeleteCoursePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class UpdateCoursePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or self.is_teacher(request.user, view))

    def is_teacher(self, user, view):
        if 'pk' in view.kwargs:
            course_id = view.kwargs['pk']
            try:
                return Course.objects.filter(Q(id=course_id) & Q(teacher__user_id=user.id)).exists()
            except Course.DoesNotExist:
                pass
        return False
