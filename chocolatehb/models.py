from django.db import models
import datetime

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    area = models.ForeignKey(Area)
    order = models.IntegerField(unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Customization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    area = models.ForeignKey(Area)
    category = models.ForeignKey(Category)
    order = models.IntegerField(unique=True)
    dependency = models.BigIntegerField(blank=True)
    instructions = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
	
class Options(models.Model):
    name = models.CharField(max_length=50)
    long_description = models.CharField(max_length=500)
    short_description = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)
    default = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    manufacturer = models.CharField(max_length=200)
    warranty = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    area = models.ForeignKey(Area)
    customization = models.ForeignKey(Customization)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class Client(models.Model):
    username = models.CharField(max_length=50)
    google_id = models.BigIntegerField()
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class House(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client)
	
class HouseOption(models.Model):
    option = models.ForeignKey(Options)
    house = models.ForeignKey(House)
    selected = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
