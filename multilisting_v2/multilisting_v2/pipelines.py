# -*- coding: utf-8 -*-
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
def store_images(house_id_val, images):
    house_id = HouseModel.objects.filter(house_id=house_id_val)
    if house_id:
        house = HouseModel.objects.get(house_id=house_id_val)
        for image in images:
            Image.objects.create(image_link=image, house=house)
    else:
        print('Cant find house with this house_id')

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
def get_data_from_dict(item):
    house_id_val = item['house_id'],
    type_of_participation_val = item['type_of_participation']
    official_builder_val = item['official_builder']
    name_of_build_val = item['name_of_build']
    decoration_val = item['decoration']
    floor_val = item['floor']
    floor_count_val = item['floor_count']
    house_type_val = item['house_type']
    num_of_rooms_val = item['num_of_rooms']
    total_area_val = item['total_area']
    living_area_val = item['living_area']
    kitchen_area_val = item['kitchen_area']
    deadline_val = item['deadline']
    phone_val = re.sub(r'[+()\- ]', '', item['phone'][0]),
    land_area_val = item['land_area']
    return deadline_val, decoration_val, floor_count_val, floor_val, house_id_val, house_type_val, kitchen_area_val, land_area_val, living_area_val, name_of_build_val, num_of_rooms_val, official_builder_val, phone_val, total_area_val, type_of_participation_val


class MultilistingV2Pipeline:
    def process_item(self, item, spider):
        if item['mode'] == 0:
            self.save_card_data(item)
        else:
            self.save_info(item)
        return item

    def save_card_data(self, item):
        house_id = item['house_id'],
        img_val = item['img']
        title_val = item['title']
        link_val = item['link']
        price_val = item['price']
        address_val = item['address']
        time_created_val = item['time_created']
        data_val = item['data']
        host_val = item['host']
        city = item['city']
        x_cord = item['cords'][0]
        y_cord = item['cords'][1]
        house_id = house_id[0]

        if HouseModel.objects.filter(house_id=house_id):
            print('This row is already exist')
        else:
            HouseModel.objects.create(house_id=house_id, title=title_val, link=link_val, address=address_val,
                                      data=data_val, time=time_created_val, Host=host_val,
                                      title_image=img_val, price=price_val, city=city, x_cord=x_cord, type=item['type'],
                                      y_cord=y_cord, offer_type = 0)

    def save_info(self, item):
        # print(item['floor_count'])
        deadline_val, decoration_val, floor_count_val, floor_val, house_id_val, house_type_val, kitchen_area_val, land_area_val, living_area_val, name_of_build_val, num_of_rooms_val, official_builder_val, phone_val, total_area_val, type_of_participation_val = get_data_from_dict(
            item)
        num_of_rooms_val = num_of_rooms_val.replace(' ', '')
        phone_val = phone_val[0]
        print(f'####{num_of_rooms_val}####')
        if floor_val == '' or floor_val == ' ':
            floor_val = 0
        if floor_count_val == ' ' or floor_count_val == '':
            floor_count_val = 0

        house_id_val = house_id_val[0]
        if HouseInfo.objects.filter(house_id=house_id_val):
            print('this row is already exist')
        else:
            store_images(house_id_val, images=item['images'])
            info = HouseInfo.objects.create(house_id=house_id_val, type_of_participation=type_of_participation_val,
                                            official_builder=official_builder_val, name_of_build=name_of_build_val,
                                            decoration=decoration_val, floor=floor_val,
                                            floor_count=floor_count_val, house_type=house_type_val,
                                            num_of_rooms=num_of_rooms_val, living_area=living_area_val,
                                            kitchen_area=kitchen_area_val, deadline=deadline_val,
                                            phone=phone_val, total_area=total_area_val, land_area=land_area_val)
            info.save()
            h_id = HouseModel.objects.filter(house_id=house_id_val)
            if h_id:
                print('Add info to house')
                house = HouseModel.objects.get(house_id=house_id_val)
                print(house_id_val, info)
                house.house_info = info
                house.data = item['data']
                house.save()
