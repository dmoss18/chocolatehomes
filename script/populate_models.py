#!/usr/bin/env python

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import sys
sys.path.append('../')
import settings

#from django.core.management import setup_environ
#from chocolatehomes import settings
#from django.conf import settings
#setup_environ(settings)

from chocolatehb.models import *

areas = ["Interior"]
categories = ["Cabinets", "Floors", "Walls", "Windows"]
customizations = ["Kitchen", "Bedroom"]

for a in areas:
    new_area = Area(name=a)
    print("Saving area: " + new_area.name)
    new_area.save()

    cat_order = 1
    for c in categories:
        cat = Category(name=c, area=new_area, order=cat_order)
        print("Saving category: " + cat.name)
        cat.save()
        cat_order += 1

        cust_order = 1
        for cu in customizations:
            cu = cu + ' ' + c
            cust = Customization(name=cu, description=cu, category=cat, order=cust_order, instructions=cu)
            print("Saving customization: " + cust.name)
            cust.save()
            cust_order += 1
            
            opts = 1
            while(opts <= 4):
                description = cu + ' ' + str(opts)
                
                opt = Option(name=description, long_description=description, short_description=description, order=opts, default=opts==1, price=10, manufacturer="Moen", warranty="1 year", customization=cust)
                print("Saving option: " + opt.name)
                opt.save()
                opts += 1
