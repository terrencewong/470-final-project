from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
