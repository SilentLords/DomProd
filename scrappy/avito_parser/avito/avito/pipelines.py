# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys

import scrapy

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from apps.base.models import HouseModel

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
links_pool = []


class AvitoPipeline:
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):

        house_id_val = item['house_id']
        img_val = item['img']
        title_val = item['title']
        link_val = item['link']
        price_val = item['price']
        address_val = item['address']
        time_created_val = item['time_created']
        data_val = item['data']
        host_val = item['host']
        city_val = item['city']
        x_cord_val = item['cords'][0]
        y_cord_val = item['cords'][1]

        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            print('This row is already exist')
        else:
            HouseModel.objects.create(house_id=house_id_val, title=title_val, link=link_val,
                                      address=address_val, data=data_val, time=time_created_val,
                                      Host=host_val, title_image=img_val, price=price_val, city=city_val,
                                      x_cord=x_cord_val, y_cord=y_cord_val)
