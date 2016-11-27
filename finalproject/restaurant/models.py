from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
	STATUS_CHOICES = (
		(CREATED, 'Order created'),
		(SENT_TO_KITCHEN, 'Order sent to kitchen'),
		(STARTED, 'Order started'),
		(READY, 'Order ready to be served'),
		(SERVED, 'Order served'),
		(COMPLETED, 'Order completed')
	)
	Code = models.CharField(max_length=20)
	Table = models.IntegerField(default=0)
	Status= models.CharField(max_length=15, choices=STATUS_CHOICES, default=CREATED,)
	StartTime = models.DateTimeField(default=timezone.now)

class MenuItem(models.Model):
	order = models.ForeignKey(Order)
	name = models.CharField(max_length=200)
	#item_id = models.CharField(max_length=20)
	#price = models.IntegerField(default=0)
	#description = models.CharField(max_length=250)
	def __str__(self):
		return self.name

class Alert(models.Model):
    Order = models.ForeignKey(Order)
    Message = models.CharField(max_length=500)
    Resolved = models.BooleanField(default=0)

class UserType(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	is_customer = models.BooleanField(default=True)
	is_kitchen = models.BooleanField(default=False)
	is_server = models.BooleanField(default=False)
    # Override the __unicode__() method to return something meaningful!
	def __unicode__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_usertype(sender,instance,created, **kwargs):
	if created:
		UserType.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_usertype(sender,instance,created, **kwargs):
	if created:
		instance.usertype.save()
