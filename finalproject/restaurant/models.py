from django.db import models
from django.utils import timezone

class Table (models.Model):
	Table = models.IntegerField(default=0)
	Code = models.CharField(max_length=20)

class Order(models.Model):
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
    Completed = models.BooleanField(default=0)
    StartTime = models.DateTimeField(default=timezone.now())
    def __str__(self):
       return self.Table

class MenuItem(models.Model):
	order = models.ForeignKey(Order)
	name = models.CharField(max_length=200)
	item_id = models.CharField(max_length=20)
	price = models.IntegerField(default=0)
	description = models.CharField(max_length=250)
	def __str__(self):
		return self.name
