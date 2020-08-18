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


def get_data_from_dict(item):
    house_id_val = item['house_id'],
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
    phone_val = re.sub(r'[+()\- ]', '', item['phone']),
    land_area_val = item['land_area']
    return deadline_val, decoration_val, floor_count_val, floor_val, house_id_val, house_type_val, kitchen_area_val, land_area_val, living_area_val, name_of_build_val, num_of_rooms_val, official_builder_val, phone_val, total_area_val, type_of_participation_val


def convert_area_vals(kitchen_area_val, land_area_val, living_area_val, total_area_val):
    if total_area_val == '':
        total_area_val = 0
    else:
        total_area_val = float("".join([x for x in total_area_val if ord(x) < 128]).replace(',','.'))
    if living_area_val == '':
        living_area_val = 0
    else:
        living_area_val = float("".join([x for x in living_area_val if ord(x) < 128]).replace(',','.'))
    if kitchen_area_val == '':
        kitchen_area_val = 0
    else:
        kitchen_area_val = float("".join([x for x in kitchen_area_val if ord(x) < 128]).replace(',','.'))
    if land_area_val == ' ':
        land_area_val = 0
    else:
        land_area_val = float("".join([x for x in land_area_val if ord(x) < 128]).replace(',','.'))
    return kitchen_area_val, land_area_val, living_area_val, total_area_val


class MailV2Pipeline:
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
                                      y_cord=y_cord, ready_to_go = True)

    def save_info(self, item):
        # print(item['floor_count'])
        deadline_val, decoration_val, floor_count_val, floor_val, house_id_val, house_type_val, kitchen_area_val, land_area_val, living_area_val, name_of_build_val, num_of_rooms_val, official_builder_val, phone_val, total_area_val, type_of_participation_val = get_data_from_dict(
            item)
        phone_val = phone_val[0]
        num_of_rooms_val = num_of_rooms_val.replace(' ', '')
        print(f'####{num_of_rooms_val}####')
        if floor_val == '' or floor_val == ' ' :
            floor_val =0
        if floor_count_val == ' ' or floor_count_val == '':
            floor_count_val = 0
        if num_of_rooms_val == ' ' or  num_of_rooms_val == '':
            pass
        else:
            print(num_of_rooms_val)
            if num_of_rooms_val == 'студии' or num_of_rooms_val == "своб. планировка":
                print('Студия или своб. планировка')
            else:
                print(num_of_rooms_val + 'hui')
                if int(num_of_rooms_val.replace(' ', '')) >= 5:
                    num_of_rooms_val = f'5к+ {num_of_rooms_val}'
                else:
                    num_of_rooms_val = f'{int(num_of_rooms_val)}к'
        kitchen_area_val, land_area_val, living_area_val, total_area_val = convert_area_vals(kitchen_area_val,
                                                                                             land_area_val,
                                                                                             living_area_val,
                                                                                             total_area_val)
        house_id_val = house_id_val[0]
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
            store_images(house_id_val, item['images'])
            info.save()
            h_id = HouseModel.objects.filter(house_id=house_id_val)
            if h_id:
                print('Add info to house')
                house = HouseModel.objects.get(house_id=house_id_val)
                print(house_id_val, info)
                house.house_info = info
                house.data = item['data']
                house.save()
