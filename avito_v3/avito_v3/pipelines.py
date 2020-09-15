# -*- coding: utf-8 -*-
import django
import os
import re
import scrapy
import sys
import requests as r
from io import BytesIO
import os
import sys

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
django.setup()
from apps.base.models import HouseModel, HouseInfo, Image

from PIL import Image as pilImage

def crop_images(image, index,house_id):
    d_file = r.get(image)
    image = BytesIO(d_file.content)
    my_image = pilImage.open(image)
    my_image.load()
    x, y = my_image.size[0], my_image.size[1]
    new_img = my_image.crop((0, 0, x, y - 50))
    new_img.save(f'/var/www/dom/src/media/{house_id}_{index}.jpg')
    return f'https://api-domafound.ru/media/{house_id}_{index}.jpg'


def store_images(house, images):
    for image in images:
        temp_img = image
        image = crop_images(image, images.index(image),house.house_id)
        if images.index(temp_img) == 0:
            house.title_image = image
            house.save()
        Image.objects.create(image_link=image, house=house)

class AvitoV3Pipeline:
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
        offer_type = item['offer_type']
        house = HouseModel.objects.filter(house_id=house_id_val)

        if house:
            print('This row is already exist')
        else:
            HouseModel.objects.create(house_id=house_id_val, title=title_val, link=link_val,
                                      address=address_val,
                                      Host=host_val, title_image=img_val, price=price_val, city=city_val,
                                      x_cord=x_cord_val, y_cord=y_cord_val, type=house_type_val, ready_to_go=False,
                                      offer_type=offer_type)

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
        phone_val = self.get_phone(house_id_val, item['headers'])
        if HouseInfo.objects.filter(house_id=house_id_val):
            house_info = HouseInfo.objects.get(house_id=house_id_val)
            if HouseModel.objects.filter(house_id=house_id_val) and not HouseInfo.objects.filter(phone=phone_val):
                house = HouseModel.objects.get(house_id=house_id_val)
                house.house_info = house_info
                house.ready_to_go = True
                house.save()
                print('Add old House info')
        else:
            if not HouseInfo.objects.filter(phone=phone_val):
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
            else:
                HouseModel.objects.get(house_id=house_id_val).delete()

    def get_phone(self, house_id, Headers):
        req = r.get(
            url=f'http://m.avito.ru/api/1/items/{house_id}/phone/?key={self.key}',
            headers=Headers)
        if re.findall('bad-request', req.content.decode("utf-8")):
            print('bad_req', req.content.decode("utf-8"))
            num = 000000000
        else:
            num = req.content.decode("utf-8").split('2B')[1].replace('"}}}', '')
        return num
