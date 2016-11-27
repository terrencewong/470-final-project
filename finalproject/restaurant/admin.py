from django.contrib import admin
from .models import Table, Order, MenuItem

# Register your models here.

admin.site.register(MenuItem)
admin.site.register(Order)