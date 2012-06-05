from chocolatehb.models import *
from django.contrib import admin

class HouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'client_email',]
    
    def client_email(self, obj):
        return obj.client.email
    client_email.short_description = 'Client email'

class OptionDependencyInline(admin.TabularInline):
    model = OptionDependency
    fk_name = "depends_on_option"
    extra = 1

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class AreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']

class CustomizationAdmin(admin.ModelAdmin):
    #fieldsets = (
    #    ('category', { 
    #        'fields': ('name', 'order')
    #    }),
    #)
    list_filter = ('category',)
    list_display = ['name', 'order', 'category']
    ordering = ['category', 'order']
    inlines = [OptionInline]

    def category_name(self, obj):
        return obj.category
    category_name.short_description = 'Category'

class OptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    #fieldsets = (
    #    (None, {
    #        'fields': ('name', 'long_description', 'short_description', 'order', 'default', 'price', 'manufacturer', 'warranty', 'customization'),
    #        'description': ('<a href=\"stuff\">To Images</a>')
    #    }),
    #)
        
    inlines = [OptionDependencyInline, ImageInline]

    def image_link(self, obj):
        return '<a href=\"stuff\">' + obj.name + '</a>'

admin.site.register(Area)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Customization, CustomizationAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Option, OptionAdmin)
