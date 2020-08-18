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


class CianV2Pipeline:
    def process_item(self, item, spider):
        if item['mode'] == 0:
            self.save_card(item)
        else:
            self.save_info(item)
        return item

    def save_card(self, item):
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

    def store_images(self, house_id_val, images):

        house_id = HouseModel.objects.filter(house_id=house_id_val)
        if house_id:
            house = HouseModel.objects.get(house_id=house_id_val)
            for image in images:
                Image.objects.create(image_link=image, house=house)
        else:
            print('Cant find house with this house_id')

    def save_info(self, item):
        house_id_val = int(item['house_id'])
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
        phone_val = re.sub(r'[+()\- ]', '', item['phone'])
        land_area_val = item['land_area']
        if not land_area_val == ' ':
            land_area_val = float(re.sub('сот.| ','', land_area_val))
        else:
            land_area_val = 0
        if floor_val == " ":
            floor_val = 0
        if floor_count_val == ' ':
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
            house_info = HouseInfo.objects.get(house_id=house_id_val)
            if HouseModel.objects.filter(house_id=house_id_val):
                house = HouseModel.objects.get(house_id=house_id_val)
                house.house_info = house_info
                house.ready_to_go = True
                house.save()
                print('Add old House info')
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
                print(house_id_val, info)
                house.house_info = info
                house.data = item['data']
                print(item['type'])
                house.type = item['type']
                house.save()
