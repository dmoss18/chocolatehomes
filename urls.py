from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('chocolatehb.views',
    (r'^$', 'index'),
    (r'^dashboard', 'dashboard'),
    (r'^admin/chocolatehb/option/(?P<option_id>\d+)/images', 'upload_images'),
    (r'^welcome', 'welcome'),
    (r'^house/(?P<house_id>\d+)/customizations/(?P<customization_id>\d+)', 'select_customization'),
    (r'^house/(?P<house_id>\d+)', 'show_house'),
    (r'^house/new', 'new_house'),
)


urlpatterns += patterns('',
    # Example:
    # (r'^chocolatehomes/', include('chocolatehomes.foo.urls')),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
