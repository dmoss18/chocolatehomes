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

class CustomizationAdmin(admin.ModelAdmin):
    list_filter = ('category',)
    inlines = [OptionInline]

class OptionAdmin(admin.ModelAdmin):
    inlines = [OptionDependencyInline]

admin.site.register(Area)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Customization, CustomizationAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(Option, OptionAdmin)
