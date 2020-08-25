# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
import django
import os
import re
import scrapy
import sys
import requests as r

DEBUG = True
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
django.setup()
from apps.base.models import HouseModel, HouseInfo, Image


def store_images(house_id_val, images):
    house_id = HouseModel.objects.filter(house_id=house_id_val)
    if house_id:
        house = HouseModel.objects.get(house_id=house_id_val)
        for image in images:
            Image.objects.create(image_link=image, house=house)
    else:
        print('Cant find house with this house_id')



class TyumenNedvizimostV1Pipeline:
    key = 'af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'

    def process_item(self, item, spider):
        print(item)
        if item['mode'] == 0:
            self.save_house(item)
        else:
            self.save_info(item)
        return item

    def save_house(self, item):
        house_id_val = item['house_id']
        img_val = item['img']
        title_val = item['title']
        link_val = item['link']
        price_val = item['price']
        address_val = item['address']
        host_val = item['host']
        city_val = item['city']
        x_cord_val = item['cords'][0]
        y_cord_val = item['cords'][1]
        house_type_val = item['house_type']
        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            print('This row is already exist')
        else:
            HouseModel.objects.create(house_id=house_id_val, title=title_val, link=link_val,
                                      address=address_val,
                                      Host=host_val, title_image=img_val, price=price_val, city=city_val,
                                      x_cord=x_cord_val, y_cord=y_cord_val, type=house_type_val,ready_to_go = False, offer_type = 0)

    def save_info(self, item):
        house_id_val = int(item['house_id'])
        type_of_participation_val = item['type_of_participation']
        official_builder_val = item['official_builder']
        name_of_build_val = item['name_of_build']
        decoration_val = item['decoration']
        house_type_val = item['house_type']
        num_of_rooms_val = item['num_of_rooms']
        total_area_val = item['total_area']
        living_area_val = item['living_area']
        kitchen_area_val = item['kitchen_area']
        floor_val = item['floor']
        floor_count_val = item['floor_count']
        land_area = item['land_area']
        data = item['data'],
        img_set = item['img_set']
        phone_val = item['phone_num']
        if HouseInfo.objects.filter(house_id=house_id_val):
            print('this row is already exist')
        else:
            info = HouseInfo.objects.create(house_id=house_id_val, type_of_participation=type_of_participation_val,
                                            official_builder=official_builder_val, name_of_build=name_of_build_val,
                                            decoration=decoration_val, floor=floor_val,
                                            floor_count=floor_count_val, house_type=house_type_val,
                                            num_of_rooms=num_of_rooms_val, living_area=living_area_val,
                                            kitchen_area=kitchen_area_val,
                                            phone=phone_val, total_area=total_area_val, land_area=land_area)
            store_images(house_id_val, img_set)
            info.save()
            print('Add info to house')
            house = HouseModel.objects.get(house_id=house_id_val)
            house.house_info = info
            house.data = data
            house.ready_to_go = True
            house.save()

