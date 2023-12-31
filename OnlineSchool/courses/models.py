from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Teacher(BaseModel):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title + ' , ' + self.teacher.user.username


class Review(BaseModel):
    SCORE_CHOICES = (
        (5, "5"),
        (4, "4"),
        (3, "3"),
        (2, "2"),
        (1, "1"),
    )

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    score = models.SmallIntegerField(choices=SCORE_CHOICES)

    def __str__(self):
        return self.user.first_name + ' , ' + self.course.title
