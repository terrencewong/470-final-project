from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Table (models.Model):
	Table = models.IntegerField(default=0)
	Code = models.CharField(max_length=20)

class Order(models.Model):
	CREATED = 'CREATED'
	SENT_TO_KITCHEN = 'SENT TO KITCHEN'
	STARTED = 'STARTED'
	READY = 'READY'
	SERVED = 'SERVED'
	COMPLETED = 'COMPLETED'
	TIMESTAMP_CHOICES = (
		(CREATED, 'Order created'),
		(SENT_TO_KITCHEN, 'Order sent to kitchen'),
		(STARTED, 'Order started'),
		(READY, 'Order ready to be served'),
		(SERVED, 'Order served'),
		(COMPLETED, 'Order completed')
	)
	Code = models.CharField(max_length=20)
	Table = models.IntegerField(default=0)
	Timestamp = models.CharField(max_length=15, choices=TIMESTAMP_CHOICES, default=CREATED,)
	StartTime = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.Table

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
