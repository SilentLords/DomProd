import re
from PIL import Image as pilImage
import requests as r
import json
import django
import os
import sys
import time

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'
sys.path.append(PATH_TO_DJANGO)

from services import get_cord

os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
django.setup()
from apps.base.models import HouseModel, HouseInfo, Image

from io import BytesIO


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
        if house.Host == 'avito.ru':
            temp_img = image
            image = crop_images(image, images.index(image),house.house_id)
            if images.index(temp_img) == 0:
                house.title_image = image
                house.save()
        Image.objects.create(image_link=image, house=house)


TOKEN = '483119792ec2155db8df5c677fa6fca8'
CITIES = ['Tюмень']
OFFERS_SET = [0, 1]
CATEGORY_SET = ['Вторичка', 'Новостройки', 'Коттеджи', 'Участки', 'Коммерческаянедвижимость']


# Сайт-источник: 1 - avito.ru, 2 - irr.ru, 3 - realty.yandex.ru, 4 - cian.ru, 5 - sob.ru, 6 - youla.io,
# 7 - n1.ru, 10 - moyareklama.ru


class Core:
    def __init__(self, host_id, category_set, city, limit):
        self.host_id = host_id
        self.category_set = category_set
        self.city = city
        self.limit = limit

    def get_data_feed(self, host, limit, city, category, offer_type):
        url = f'https://ads-api.ru/main/api?user=mr.niki002@gmail.com&token={TOKEN}&limit={limit}&city=Тюмень&person_type=3&source={host}&category_id={category}&nedvigimost_type={offer_type}'
        response = r.get(url)
        result = json.loads(response.content)['data']
        for res in result:
            final_res = self.correct(res, category, offer_type - 1)
            self.save_data(final_res)
        return result

    def correct(self, result, category, offer_type, ):
        num_of_rooms = type_ = house_type = address = ''
        floor = floor_count = total_area = kitchen_area = living_area = land_area = 0
        if category == 2:
            if offer_type == 0:
                num_of_rooms = self.correct_num_of_rooms(result, 'param_1945')
                type_ = self.correct_type(result, 'param_1957')
                try:
                    house_type = result['param_2009']
                except:
                    pass
                floor = result['param_2113']
                floor_count = result['param_2213']
                total_area = float(result['param_2313'])
                address = result['address']

                try:
                    kitchen_area = float(result['param_2314'])
                except:
                    pass
                try:
                    living_area = float(result['param_12722'])
                except:
                    pass
            else:
                num_of_rooms = self.correct_num_of_rooms(result, 'param_2019')
                type_ = 'Вторичка'
                try:
                    house_type = result['param_2078']
                except:
                    pass
                floor = result['param_2315']
                floor_count = result['param_2415']
                try:
                    total_area = float(result['param_2515'])
                except:
                    pass
                address = result['address']
                try:
                    kitchen_area = float(result['param_12723'])
                except:
                    pass
                try:
                    living_area = float(result['param_12724'])
                except:
                    pass
        elif category == 4:
            if offer_type == 0:
                try:
                    floor_count = result['param_3837']
                except:
                    pass
                type_ = 'Коттеджи'
                try:
                    house_type = result['param_3843']
                except:
                    pass
                try:
                    total_area = float(result['param_4014'])
                except:
                    pass
                try:
                    land_area = float(result['param_4015'])
                except:
                    pass
            else:
                try:
                    floor_count = result['param_4016']
                except:
                    pass
                type_ = 'Коттеджи'
                try:
                    house_type = result['param_4022']
                except:
                    pass
                try:
                    total_area = float(result['param_4193'])
                except:
                    pass
                try:
                    land_area = float(result['param_4194'])
                except:
                    pass
        elif category == 5:
            if offer_type == 0:
                type_ = 'Участки'
                try:
                    land_area = float(result['param_4616'])
                except:
                    pass
            else:
                type_ = 'Участки'
                try:
                    land_area = float(result['param_4194'])
                except:
                    pass
        elif category == 7:
            if offer_type == 0:
                try:

                    floor_count = result['param_12869']
                except:
                    pass
                type_ = 'Коммерческаянедвижимость'
                try:
                    total_area = float(result['param_4920'])
                except:
                    pass
                try:
                    floor = result['param_12868']
                except:
                    pass
            else:
                try:
                    floor_count = result['param_12881']
                except:
                    pass
                type_ = 'Коммерческаянедвижимость'
                try:
                    total_area = float(result['param_4922'])
                except:
                    pass
                try:
                    floor = result['param_12880']
                except:
                    pass

        address = result['address']
        address = result['city'] + ' ' + address
        price = result['price']
        cords = [0, 0]
        try:
            cords = [result['cords']['lat'], result['cords']['lng']]
        except:
            cords[1], cords[0], _ = get_cord(address)

        title = result['title']
        description = result['description']
        host = result['source']
        phone = result['phone']
        link = result['url']
        images = []
        for img in result["images"]:
            images.append(img['imgurl'])
            # TODO Написать сохранение фоток для того что бы резать знаки
        if not phone[0] == '7':
            phone = '7' + phone[1:]
        if len(images) > 0:
            title_image = images[0]
        else:
            title_image = ''
        try:
            house_id = result['avitoid']
        except:
            house_id = result['id']
        data = {'num_of_rooms': num_of_rooms, 'type': type_, 'house_type': house_type, 'floor': floor,
                'floor_count': floor_count, 'total_area': total_area, 'kitchen_area': kitchen_area,
                "living_area": living_area, 'address': address, 'land_area': land_area, 'images': images,
                'price': price, 'cords': cords, 'title': title, 'description': description, "host": host,
                'phone': phone, 'title_image': title_image, 'link': link, 'offer_type': offer_type,
                'house_id': house_id}

        return data

    def correct_type(self, result, selector):
        type_ = result[selector]
        if type_ == 'Новостройка':
            type_ = 'Новостройки'
        return type_

    def correct_num_of_rooms(self, result, selector):
        num_of_rooms = result[selector]
        if not (num_of_rooms == 'Студия'):
            if int(num_of_rooms) > 5:
                num_of_rooms = f'{num_of_rooms}к+ {num_of_rooms}'
            else:
                num_of_rooms = f'{num_of_rooms}к'
        else:
            num_of_rooms = 'cтудии'
        return num_of_rooms

    def save_data(self, data):
        try:
            house = HouseModel.objects.filter(house_id=data['house_id'])
        except:
            data['house_id'] = re.sub(r'[^0-9]', '', data['house_id'])

            house = HouseModel.objects.filter(house_id=data['house_id'])
        if not house and not HouseModel.objects.filter(house_info__phone=data['phone']):
            house_info = HouseInfo.objects.create(house_id=data['house_id'],
                                                  type_of_participation='',
                                                  official_builder='',
                                                  name_of_build='',
                                                  decoration='', floor=data['floor'],
                                                  floor_count=data['floor_count'], house_type=data['house_type'],
                                                  num_of_rooms=data['num_of_rooms'], living_area=data['living_area'],
                                                  kitchen_area=data['kitchen_area'],
                                                  phone=data['phone'], total_area=data['total_area'],
                                                  land_area=data['land_area'])
            house = HouseModel.objects.create(house_id=data['house_id'], title=data['title'], link=data['link'],
                                              address=data['address'],
                                              Host=data['host'], title_image=data['title_image'], price=data['price'],
                                              city=0,
                                              x_cord=data['cords'][1], y_cord=data['cords'][0], type=data['type'],
                                              ready_to_go=True,
                                              offer_type=data['offer_type'], house_info=house_info,
                                              data=data['description'])
            store_images(house, images=data['images'])

    def start(self):
        for offer_type in OFFERS_SET:
            for category in self.category_set:
                self.get_data_feed(self.host_id, self.limit, self.city, category, offer_type + 1)
                time.sleep(5)
