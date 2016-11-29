# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models


class menu(models.Model):
  
    Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=200)
    Nutrition = models.CharField(max_length=200)
    Price = models.IntegerField(default=170)
class specialmenu(models.Model):
    Name = models.CharField(max_length=200)
    Description = models.CharField(max_length=200)
    Nutrition = models.CharField(max_length=200)
    Price = models.IntegerField(default=170)