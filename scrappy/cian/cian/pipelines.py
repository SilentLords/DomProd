# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import re

from apps.base.models import HouseModel

sys.path.append('/var/www/dom/src/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django


class CianPipeline:
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        house_id_val = int(re.sub(r'\?osale1|\?osale2', '', item['house_id']))
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
        x_cord_val = item['cords'][0]
        y_cord_val = item['cords'][1]
        if HouseModel.objects.filter(house_id=house_id_val):
            print('This row is already exist')
        else:
            HouseModel.objects.create(house_id=house_id_val, title=title_val, link=link_val, address=address_val,
                                      data=data_val, time=time_created_val, Host=host_val,
                                      title_image=img_val, price=price_val, city=city_val, type=type_,
                                      x_cord=x_cord_val, y_cord=y_cord_val)
