from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Table (models.Model):
	Table = models.IntegerField(default=0)
	Code = models.CharField(max_length=20)	

class Order(models.Model):
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
    Completed = models.BooleanField(default=0)
    #StartTime = models.DateTimeField(default=timezone.now())
	
class MenuItem(models.Model):
	Code = models.CharField(max_length=20)
	Item_id = models.CharField(max_length=20)
	Item_name = models.CharField(max_length=50)
	Price = models.IntegerField(default=0)
	Description = models.CharField(max_length=250)
	def __str__(self):
		return self.Item_name
	