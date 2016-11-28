from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from menu.models import menu

# Create your models here.

class Table (models.Model):
	Table = models.IntegerField(default=0)
	Code = models.CharField(max_length=20)	

class Order(models.Model):
    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
    Completed = models.BooleanField(default=0)
    StartTime = models.DateTimeField(default=timezone.now())
	
class MenuItem(models.Model):
	order = models.ForeignKey(Order)
	name = models.CharField(max_length=200)
	#item_id = models.CharField(max_length=20)
	#price = models.IntegerField(default=0)
	#description = models.CharField(max_length=250)
	def __str__(self):
		return self.name

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username

class OrderedMenuItems(models.Model):
	order_id = models.ForeignKey(Order)
	#table_id = models.ForeignKey(Order)
	item_name = models.ForeignKey(menu)
	num_items = models.IntegerField(default=0)#, null=True)
	notes = models.TextField(max_length=500)
	def __str__(self):
		return self.item_name