#!/bin/bash

from __future__ import print_function
import os
import MySQLdb
import dateutil.parser
from datetime import datetime, date
import requests
import time
import json
import database


mlurl = os.environ['ML_URL']
debug = os.environ.get('DEBUG', False)
categories = os.environ['CATEGORIES'].split(',')

db_host = os.getenv('DATABASE_SERVICE_NAME', 'localhost')
db_port = int(os.getenv('MYSQL_PORT', '3306'))
db_user = os.getenv('MYSQL_USER', 'root')
db_passwd = os.getenv('MYSQL_PASSWORD', 'root')
db_name = os.getenv('MYSQL_DATABASE', 'ml')
conn = MySQLdb.connect(host=db_host, user=db_user, port=db_port,
                    passwd=db_passwd,db=db_name)

now = datetime.utcnow()

def make_item(item):
    return {
        'item': item['id'],
        'timestamp': now,
        'title': item['title'].encode('utf-8'),
        'price': item['price'],
        'sold_quantity': item['sold_quantity'],
        'available_quantity': item['available_quantity'],
        'seller': item['seller']['id']
    }

def getitems(category):

    url = mlurl+'/sites/MLA/search?category='+category+'&limit=200'
    r = requests.get(url)
    r = r.json()
    for item in r['results']:
        database.insert(conn, 'items', make_item(item))


def make_seller(seller):
    return {
        'seller': seller['id'],
        'timestamp': now,
        'nickname': seller['nickname'],
        'city': seller['address']['city'].encode('utf-8'),
        'state': seller['address']['state'].encode('utf-8'),
        'canceled_transactions': seller['seller_reputation']['transactions']['canceled'],
        'completed_transactions': seller['seller_reputation']['transactions']['completed'],
        'reputation': seller['seller_reputation']['power_seller_status']
    }


def getsellers():
    data = database.getsellers(conn)
    for i in data:
        url = mlurl+'/users/'+str(i['seller'])
        r = requests.get(url)
        database.insert(conn, 'seller', make_seller(r.json()))

for c in categories:
    getitems(c)

getsellers()
