from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Course, Teacher, Review
from .permissions import *
from .serializers import CourseSerializer, TeacherSerializer, ReviewSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().order_by('published_at')
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        """
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [CreateOrDeleteCoursePermissions]
        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = [UpdateCoursePermissions]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    @action(detail=True)
    def courses(self, request, pk=None):
        teacher = self.get_object()
        courses = Course.objects.filter(teacher=teacher)

        page = self.paginate_queryset(courses)
        if page is not None:
            serializer = CourseSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class ReviewViewSet(GenericViewSet, ListModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Review.objects.filter(user=self.request.user)
        return queryset
