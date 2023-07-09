from django.db.models import Avg
from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Course, Teacher, Review


class CourseSerializer(serializers.ModelSerializer):
    num_reviews = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()

    def get_num_reviews(self, obj):
        return Review.objects.filter(course=obj.id).count()

    def get_avg_score(self, obj):
        return Review.objects.filter(course=obj.id).aggregate(Avg('score'))['score__avg'] or 0

    def validate_price(self, value):
        if value < 10000:
            raise serializers.ValidationError("Price must be at least 10,000 tomans.")
        return value

    def create(self, validated_data):
        self.validate_price(validated_data.get('price'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.validate_price(validated_data.get('price', instance.price))
        return super().update(instance, validated_data)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'teacher', 'price', 'published_at', 'num_reviews', 'avg_score')


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Review
        fields = "__all__"
