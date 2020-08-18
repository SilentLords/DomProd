# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import re

from apps.base.models import HouseModel
DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django


class BarahlaPipeline:
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        house_id_val = re.sub(r'\?osale1|\?osale2','',item['house_id'])
        img_val = item['img']
        title_val = item['title']
        link_val = item['link']
        price_val = item['price']
        address_val = item['address']
        time_created_val = item['time_created']
        data_val = item['data']
        host_val = item['host']
        city_val = item['city']
        type_ = item['type']
        print(house_id_val)
        print('there')
        if HouseModel.objects.filter(house_id=house_id_val):
            print('This row is already exist')
        else:
            print('house_id_val:'+house_id_val, 'title_val:'+title_val, 'link_val:'+link_val, 'address_val:'+address_val,
                                      'data_val:'+data_val, 'time_created_val:'+time_created_val, 'host_val:'+host_val,
                                      'img_val:'+img_val, 'price_val:'+price_val, 'city_val:'+city_val, 'type_:'+type_)
            HouseModel.objects.create(house_id=house_id_val, title=title_val, link=link_val, address=address_val,
                                      data=data_val, time=time_created_val, Host=host_val,
                                      title_image=img_val, price=price_val, city=city_val, type=type_)
