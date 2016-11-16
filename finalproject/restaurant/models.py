#REFERNCE INFO:
#https://docs.djangoproject.com/en/1.10/ref/models/fields/
#   https://docs.djangoproject.com/en/1.10/ref/models/fields/#foreignkey
#       https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models.ForeignKey.on_delete
#http://www.pshrmn.com/tutorials/django/models/

from django.db import models

################################################################################################################################################################

class Restaurant(models.Model):
    restaurantId   = models.AutoField(primary_key=True)
    name           = models.CharField(max_length=256)
    telephone      = models.CharField(max_length=256, blank=True)
    website        = models.URLField(max_length=256, blank=True)
    #Address:
    unitNumber     = models.CharField(max_length=6, blank=True)
    buildingNumber = models.CharField(max_length=6, blank=True)
    streetName     = models.CharField(max_length=256, blank=True)
    city           = models.CharField(max_length=256, blank=True)
    province       = models.CharField(max_length=256, blank=True)
    postalCode     = models.CharField(max_length=6, blank=True)

class RestaurantHasMenu(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menuId       = models.ForeignKey(Menu, on_delete=models.CASCADE)

class Menu(models.Model):
    menuId      = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256, blank=True)

class MenuHasItem(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    menuId      = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menuItemId  = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

class MenuItem(models.Model):
    menuItemId  = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=256)
    price       = models.DecimalField(decimal_places=2)
    description = models.TextField()

################################################################################################################################################################

from django.core.validators import EmailValidator

class User(models.Model):
    userId       = models.AutoField(primary_key=True)
    username     = models.CharField(max_length=256)
    passwordHash = models.CharField(max_length=1024)
    firstName    = models.CharField(max_length=256)
    surname      = models.CharField(max_length=256)
    emailAddress = models.EmailField(max_length=256)

class Customer(models.Model):
    customerId      = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    loyaltyPoints   = models.PositiveIntegerField(default=0)
    seatedAtTableId = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)

class Waiter(models.Model):
    waiterId        = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, unique=True)

class Cook(models.Model):
    cookId          = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, unique=True)

class Manager(models.Model):
    managerId       = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True, unique=True)

################################################################################################################################################################

class WaiterWorksAtRestaurant(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    waiterId     = models.ForeignKey(Waiter, on_delete=models.CASCADE)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class CookWorksAtRestaurant(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    cookId       = models.ForeignKey(Cook, on_delete=models.CASCADE)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

class ManagerManagesRestaurant(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    managerId    = models.ForeignKey(Manager, on_delete=models.CASCADE)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

################################################################################################################################################################

class Table(models.Model):
    tableId               = models.AutoField(primary_key=True)
    belongsToRestaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE, unique=True)
    servedByWaiterId      = models.ForeignKey(Waiter, null=True, on_delete=models.SET_NULL)

################################################################################################################################################################

class Order(models.Model):
    #A default primary key called 'id', with type AutoField, is it automatically created, since one is not explicity defined.
    #Django does NOT support keys that are made up of multiple fields.
    placedByCustomerId = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    orderedMenuItemId  = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    randomCode         = models.CharField(max_length=6, blank=True)
    dateTimeOrdered    = models.DateTimeField(auto_now=True)
    completed          = models.BooleanField(default=False)


