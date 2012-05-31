from django.db import models
import datetime

# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    area = models.ForeignKey(Area)
    order = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Customization(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    area = models.ForeignKey(Area)
    category = models.ForeignKey(Category)
    order = models.IntegerField(unique=True)
    depends_on_customization = models.ForeignKey('self', blank=True, null=True)
    instructions = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Option(models.Model):
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
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Client(models.Model):
    username = models.CharField(max_length=50)
    google_id = models.BigIntegerField()
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.username

class House(models.Model):
    name = models.CharField(max_length=50)
    client = models.ForeignKey(Client)
    options = models.ManyToManyField(Option, through='HouseOption')
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class HouseOption(models.Model):
    option = models.ForeignKey(Option)
    house = models.ForeignKey(House)
    selected = models.BooleanField(default=False)
    customization_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)

class OptionDependency(models.Model):
    depends_on_option = models.ForeignKey(Option, related_name="depends_on_option")
    available_option = models.ForeignKey(Option, related_name="available_option")
    customization_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
