from django.db import models

class Order(models.Model):
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)

class MenuItem(models.Model):
    order = models.ForeignKey(Order)
    name = models.CharField(max_length=200)
