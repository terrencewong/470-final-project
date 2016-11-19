# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import menu

class menuAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Description', 'Nutrition', 'Price')

admin.site.register(menu, menuAdmin)