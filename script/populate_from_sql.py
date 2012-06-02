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
from django.db import connection, transaction
    
cursor = connection.cursor()

file = open("sql/insert_data.sql")
while 1:
    line = file.readline()
    if not line:
        break

    print(line)
    # Data modifying operation - commit required
    cursor.execute(line)
    transaction.commit_unless_managed()
