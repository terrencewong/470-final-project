from django.contrib import admin
<<<<<<< HEAD
from .models import Table, Order
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
=======
from .models import Table, Order, MenuItem
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
from restaurant.models import UserType
# Register your models here.

'''
Extended User model reference:
https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#extending-user
'''
# Define an inline admin descriptor for UserType model
# which acts a bit like a singleton
class UserTypeInline(admin.StackedInline):
    model = UserType
    can_delete = False
    verbose_name_plural = 'usertype'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserTypeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
<<<<<<< HEAD
=======
admin.site.register(MenuItem)
>>>>>>> caca943b08e3c9846d830490d7045b695ad02803
admin.site.register(Order)
