from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Table (models.Model):
	Table = models.IntegerField(default=0)
	Code = models.CharField(max_length=20)

class Order(models.Model):
	CREATED = 'CRE'
	SENT_TO_KITCHEN = 'STK'
	STARTED = 'STA'
	READY = 'RDY'
	SERVED = 'SER'
	TIMESTAMP_CHOICES = (
		(CREATED, 'Order created'),
		(SENT_TO_KITCHEN, 'Order sent to kitchen'),
		(STARTED, 'Order started'),
		(READY, 'Order ready to be served'),
		(SERVED, 'Order served'),
	)

    Code = models.CharField(max_length=20)
    Table = models.IntegerField(default=0)
	Timestamp_choices = models.CharField(max_length=3, choices=Timestamp_choices, default=CREATED,)
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
