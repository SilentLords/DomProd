# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import re

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


class InfoPipeline:
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_images(self, house_id_val, images):

        house_id = HouseModel.objects.filter(house_id=house_id_val)
        if house_id:
            house = HouseModel.objects.get(house_id=house_id_val)
            for image in images:
                Image.objects.create(image_link=image, house=house)
        else:
            print('Cant find house with this house_id')

    def store_db(self, item):
        # print(item['floor_count'])
        house_id_val = int(item['house_id'].replace(' ', '').split('?')[0])
        type_of_participation_val = item['type_of_participation']
        official_builder_val = item['official_builder']
        name_of_build_val = item['name_of_build']
        decoration_val = item['decoration']
        floor_val = item['floor']
        floor_count_val = item['floor_count']
        house_type_val = item['house_type']
        num_of_rooms_val = item['num_of_rooms'].replace(' ', '')
        total_area_val = item['total_area'].replace('м²', '').strip().replace(',', '.')
        living_area_val = item['living_area'].replace('м²', '').strip().replace(',', '.')
        kitchen_area_val = item['kitchen_area'].replace('м²', '').strip().replace(',', '.')
        deadline_val = item['deadline']
        phone_val = re.sub(r'[+()\-\n ]', '', item['phone'])
        x_cord_val = item['cords'][0]
        y_cord_val = item['cords'][1]
        if x_cord_val and y_cord_val:
            pass
        else:
            x_cord_val = y_cord_val = None
        if not item['address']:
            item['address'] = ''
        floor_val = 0
        floor_count_val = 0
        if total_area_val == '':
            total_area_val = 0
        else:
            total_area_val = float("".join([x for x in total_area_val if ord(x) < 128]))
        if living_area_val == '':
            living_area_val = 0
        else:
            living_area_val = float("".join([x for x in living_area_val if ord(x) < 128]))
        if kitchen_area_val == '':
            kitchen_area_val = 0
        else:
            kitchen_area_val = float("".join([x for x in kitchen_area_val if ord(x) < 128]))
        if HouseInfo.objects.filter(house_id=house_id_val):
            print(HouseInfo.objects.get(house_id=house_id_val).house_id, house_id_val)
            print('this row is already exist')
        else:
            info = HouseInfo.objects.create(house_id=house_id_val, type_of_participation=type_of_participation_val,
                                            official_builder=official_builder_val, name_of_build=name_of_build_val,
                                            decoration=decoration_val, floor=floor_val,
                                            floor_count=floor_count_val, house_type=house_type_val,
                                            num_of_rooms=num_of_rooms_val, living_area=living_area_val,
                                            kitchen_area=kitchen_area_val, deadline=deadline_val,
                                            phone=phone_val, total_area=total_area_val)
            self.store_images(house_id_val, item['images'])
            info.save()
            h_id = HouseModel.objects.filter(house_id=house_id_val)
            if h_id:
                print('Add info to house')
                house = HouseModel.objects.get(house_id=house_id_val)
                house.house_info = info
                house.type = item['type']
                house.data = item['data']
                house.address = item['address']
                house.x_cord = x_cord_val
                house.y_cord = y_cord_val
                # house.type = item['type']
                house.save()
