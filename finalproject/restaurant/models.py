from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User)
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
    Completed = models.BooleanField(default=0)
    StartTime = models.DateTimeField(default=timezone.now())

class MenuItem(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
