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


####
###
##Clear out any old data that might exist
#
areas_to_delete = Area.objects.all()
#Deleting an area should delete all its dependent children (category, customization, option, houseoption, image)
for a in areas_to_delete:
    print("Deleting area: " + a.name)
    a.delete()

page_types_to_delete = PageType.objects.all()
#Deleting a pagetype should delete all its dependent children (customization, imagetype, image)
for p in page_types_to_delete:
    print("Deleting pagetype: " + p.name)
    p.delete()




####
###
##Populate database with new values
#
page_types = ["Full Page", "Pallette Page", "Tile Page"]
full_page = ["mainThumb", "mainLarge"]
pallette_page = ["Swatch", "Large"]
tile_page = ["Tile", "Large"]

pTypesList = []

for p in page_types:
    pType = PageType(name=p)
    print("Saving PageType: " + pType.name)
    pType.save()
    pTypesList.append(pType)

#Full Page Image Type Creation
p = pTypesList[0]
iwidth=50
iheight=50
iType = ImageType(name=full_page[0], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()
iType = ImageType(name=full_page[1], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()

x = 1
#while(x <= 4):
iType = ImageType(name="alt" + str(x) + "Large", page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()
iType = ImageType(name="alt" + str(x) + "Thumb", page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()

#Pallette Page Image Type Creation
p = pTypesList[1]
iType = ImageType(name=pallette_page[0], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()
iType = ImageType(name=pallette_page[1], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()

#Tile Page Image Type Creation
p = pTypesList[2]
iType = ImageType(name=tile_page[0], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()
iType = ImageType(name=tile_page[1], page_type=p, width=iwidth, height=iheight)
print("Saving ImageType: " + iType.name)
iType.save()




areas = ["Interior"]
categories = ["Cabinets", "Floors", "Walls", "Windows"]
customizations = ["Kitchen", "Bedroom"]

for a in areas:
    #new_area = Area.objects.get(name=a)
    #if new_area:
    #    break

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
        cust_pType = True
        for cu in customizations:
            if cust_pType:
                #Full page
                p = PageType.objects.get(name=page_types[0])
            else:
                #Pallette Page
                p = PageType.objects.get(name=page_types[1])

            cu = cu + ' ' + c
            cust = Customization(name=cu, description=cu, category=cat, order=cust_order, instructions=cu, page_type=p)
            print("Saving customization: " + cust.name)
            cust.save()
            cust_order += 1

            cust_pType = not cust_pType
            
            opts = 1
            while(opts <= 4):
                description = cu + ' ' + str(opts)
                
                opt = Option(name=description, long_description=description, short_description=description, order=opts, default=opts==1, price=10, manufacturer="Moen", warranty="1 year", customization=cust)
                print("Saving option: " + opt.name)
                opt.save()
                opts += 1
