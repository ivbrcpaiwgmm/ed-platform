from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    class Meta:
        abstract = True


class Product(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_group_size = models.PositiveSmallIntegerField()
    max_group_size = models.PositiveSmallIntegerField()


class Lesson(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    video_url = models.URLField()


class Group(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
