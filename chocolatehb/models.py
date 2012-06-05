from django.db import models
import datetime

# Create your models here.
class PageType(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)

    def __unicode__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)
    area = models.ForeignKey(Area)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ['area', 'order']
        ordering = ['area', 'order']
        order_with_respect_to = 'area'
        verbose_name_plural = "categories"

class Customization(models.Model):
    name = models.CharField(max_length=50, unique=False)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category)
    order = models.IntegerField()
    depends_on_customization = models.ForeignKey('self', blank=True, null=True)
    instructions = models.CharField(max_length=500)
    page_type = models.ForeignKey(PageType)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ['category', 'order']
        ordering = ['category']
        order_with_respect_to = 'category'

class Option(models.Model):
    name = models.CharField(max_length=50)
    long_description = models.CharField(max_length=500)
    short_description = models.CharField(max_length=100)
    order = models.IntegerField()
    default = models.BooleanField(default=False)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    manufacturer = models.CharField(max_length=200)
    warranty = models.CharField(max_length=200)
    customization = models.ForeignKey(Customization)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ['customization', 'order']
        ordering = ['customization', 'order']
        order_with_respect_to = 'customization'

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

class ImageType(models.Model):
    name = models.CharField(max_length=10)
    page_type = models.ForeignKey(PageType)
    width = models.IntegerField()
    height = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.name

class Image(models.Model):
    original_name = models.CharField(max_length=50)
    name = models.CharField(unique=True, max_length=50)
    image_type = models.ForeignKey(ImageType)
    option = models.ForeignKey(Option)
    created_at = models.DateTimeField(auto_now_add = True, auto_now = False)
    updated_at = models.DateTimeField(auto_now_add = True, auto_now = True)
    def __unicode__(self):
        return self.original
