from django.db import models

class Order(models.Model):
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
    Completed = models.BooleanField(default=0)
    StartTime = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.Table
