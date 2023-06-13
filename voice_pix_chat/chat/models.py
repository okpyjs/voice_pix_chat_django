from basic.models import AutoDate
from django.db import models


# Create your models here.
class TestModel(models.Model, AutoDate):
    name = models.CharField(max_length=200, default="name")
    count = models.IntegerField()
