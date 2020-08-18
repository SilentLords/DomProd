# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
import os
import sys

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from apps.base.models import HouseModel, Image, HouseInfo


class N1V2Pipeline:
    def process_item(self, item, spider):
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
                                      x_cord=x_cord_val, y_cord=y_cord_val, ready_to_go = True)

    def save_info(self, item):
        house_id_val = int(item['house_id'])
        type_of_participation_val = item['type_of_participation']
        official_builder_val = item['official_builder']
        name_of_build_val = item['name_of_build']
        decoration_val = item['decoration']
        floor_val = item['floor']
        floor_count_val = item['floor_count']
        house_type_val = item['house_type']
        num_of_rooms_val = item['num_of_rooms'].replace('-', '')
        total_area_val = item['total_area']
        living_area_val = item['living_area']
        kitchen_area_val = item['kitchen_area']
        land_area_val = item['land_area']
        deadline_val = item['deadline']
        phone_val = int(item['phone'].replace(' ', ''))
        if num_of_rooms_val == 'студии' or num_of_rooms_val == "своб. планировка":
            print('Студия или своб. планировка')
        else:
            if int(num_of_rooms_val.split('к')[0]) >= 5:
                num_of_rooms_val = f"5к+ {int(num_of_rooms_val.split('к')[0])}"
        if HouseInfo.objects.filter(house_id=house_id_val):
            print('this row is already exist')
        else:
            info = HouseInfo.objects.create(house_id=house_id_val, type_of_participation=type_of_participation_val,
                                            official_builder=official_builder_val, name_of_build=name_of_build_val,
                                            decoration=decoration_val, floor=floor_val,
                                            floor_count=floor_count_val, house_type=house_type_val,
                                            num_of_rooms=num_of_rooms_val, living_area=living_area_val,
                                            kitchen_area=kitchen_area_val, deadline=deadline_val,
                                            phone=phone_val, total_area=total_area_val, land_area=land_area_val)
            self.store_images(house_id_val, item['images'])
            info.save()
            h_id = HouseModel.objects.filter(house_id=house_id_val)
            if h_id:
                print('Add info to house')
                house = HouseModel.objects.get(house_id=house_id_val)
                house.house_info = info
                house.data = item['data']
                house.type = item['type']
                house.save()

    def store_images(self, house_id_val, images):

        house_id = HouseModel.objects.filter(house_id=house_id_val)
        if house_id:
            house = HouseModel.objects.get(house_id=house_id_val)
            for image in images:
                Image.objects.create(image_link=image, house=house)
        else:
            print('Cant find house with this house_id')
