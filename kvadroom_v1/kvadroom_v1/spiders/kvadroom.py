# -*- coding: utf-8 -*-

import django
import os
import re
import scrapy
import sys

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = 'C:/Users/nick/PycharmProjects/Domafound/'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
django.setup()
from services import get_cord
from apps.base.models import HouseModel, CITY_CHOICES


#
def get_house_id(url):
    if url.split("._").__len__() > 2:
        h_id = re.sub(r'[^0-9]', '', url.split("._")[2])
    else:
        if url.split("._").__len__() == 1:
            h_id = re.sub(r'[^0-9]', '', url.split("_")[-1])
        else:
            h_id = re.sub(r'[^0-9]', '', url.split("._")[1])
    return h_id


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


def correct_price(text):
    if text.find('млн') > -1:
        return int(re.sub(r'[^0-9]', '', text)) * 1000000
    else:
        return int(re.sub(r'[^0-9]', '', text))


def get_house_type(house_id):
    try:
        return HouseModel.objects.get(house_id=house_id).type
    except:
        return ''


def delete_house_model(house_id):
    HouseModel.objects.filter(house_id=house_id).delete()


class KvadroomSpider(scrapy.Spider):
    name = 'kvadroom'
    allowed_domains = ['kvadroom.ru']
    urls_pool = [
        'https://tum.kvadroom.ru/tyumen/kupit-kvartiru/',
        'https://tum.kvadroom.ru/tyumen/kupit-dom/',
        'https://tum.kvadroom.ru/tyumen/zemelnie-uchastki/'
    ]
    start_urls = [urls_pool[0]]
    parsing_params = {
        'card_to_parse': 2,
        'card_selector': '.ci_3_col',
        'house_type_set': ['Вторичка', 'Коттеджи', 'Участки'],
        'ignore_selector': '.ci_3__owner__info > div::text',
        'link_selector': 'a.ci_3__link::attr(href)',
        'address_selector': '.ci_3__col-main_info > p::text',
        'title_image_selector': '.ci_3__slider::attr(data-imgs)',
        'title_selector': 'h3.snippet-title >a > span::text',
        'price_selector': 'li.ci_3__price::text'
    }
    parsing_info_params = {'image_set_selector': '.ob2_slider > .js_ob2_slider_imgs > span',
                           'image_data_selector': '::attr(data-src)',
                           'data_selectors': '.ob2_descr__text_content > div > p::text',
                           'views_selector': '.ob2_icon-viewed::text',
                           'info_selectors': '.u_ob2_dot_list > li',
                           'phone_num_selector': '.js_show_all_phone::attr(data-link-tel)'
                           }

    def parse(self, response):
        page_index = self.urls_pool.index(response.url)
        cards = response.css(self.parsing_params['card_selector'])
        print(f'Processing: {response.url}')
        type_of_house = self.parsing_params['house_type_set'][page_index]
        counter = 0
        for correct_card in cards:
            ignore_tag = correct_card.css(self.parsing_params['ignore_selector'])
            if ignore_tag:
                # print(ignore_tag[1])
                if not ignore_tag[0].css('::text').get() == 'Наш партнер':
                    cards.pop(cards.index(correct_card))
                    counter += 1
        print(f'Deleted lines: {counter}')
        for card in cards:
            if cards.index(card) < self.parsing_params['card_to_parse']:
                house_link = response.urljoin(card.css(self.parsing_params['link_selector']).get())
                house_id = get_house_id(house_link)
                if check_db(house_id):
                    _ = yield from self.parse_card(card, type_of_house, house_id, house_link, page_index)
                    yield scrapy.Request(url=house_link, callback=self.parse_info)
                else:
                    print('This house is already exist')
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)

    def get_views_count(self, response):
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).getall()[-1]
                                 .split(' ')[0]))
        return views_count

    def parse_card(self, card, type_of_house, house_id, link, page_index=0):
        city = 0
        if 0 <= page_index < 3:
            city = 0
        address = ' '.join(card.css(self.parsing_params['address_selector']).getall())
        x_cord, y_cord, address = get_cord(address)
        title_image = card.css(self.parsing_params['title_image_selector']).get().split(',')[0]
        title = type_of_house + " " + address
        price = correct_price(card.css(self.parsing_params['price_selector']).get())
        item = {
            'mode': 0,
            'house_id': house_id,
            'img': title_image,
            'title': title,
            'link': link,
            'price': price,
            'address': address,
            'host': self.allowed_domains[0],
            'city': city,
            'cords': [x_cord, y_cord],
            'house_type': type_of_house
        }
        yield item
        return ''

    def parse_info(self, response):

        house_id = get_house_id(response.url)
        views_count = int(re.sub(r'[^0-9]', '', response.css(self.parsing_info_params['views_selector']).getall()[-1]
                                 .split(' ')[0]))
        print(views_count)
        if views_count <= 100:
            floor = floor_count = total_area = living_area = kitchen_area = land_area = 0
            name_of_build = data = num_of_rooms = decoration = official_builder = type_of_participation = house_type = ''
            type_ = get_house_type(house_id)
            image_set = response.css(self.parsing_info_params['image_set_selector'])
            images = []
            for image in image_set: images.append(
                image.css(self.parsing_info_params["image_data_selector"]).get())

            data = response.css(self.parsing_info_params['data_selectors']).get()

            query_selector = self.parsing_info_params['info_selectors']
            for info in response.css(query_selector):
                value_of_field = info.css('::text').getall()
                #     name_of_field = values[0]
                if not value_of_field.__len__() > 1:
                    value_of_field = value_of_field[0]
                    print(value_of_field)
                    if re.search(r'Участок', value_of_field):
                        land_area = float(re.sub(r'[^0-9.]', '', value_of_field))

                    if re.search(r'этаж', value_of_field):
                        value_of_field = re.sub(r'[^0-9из]', '', value_of_field)
                        floor = int(value_of_field.split('из')[0])
                        floor_count = int(value_of_field.split('из')[1])
                    if re.search(r'-x', value_of_field):
                        num_of_rooms = value_of_field.replace(' ', '')

                        if num_of_rooms == 'студии' or num_of_rooms == "своб.планировка":
                            print('Студия или своб. планировка')
                        else:
                            if int(num_of_rooms.split('-')[0]) >= 5:
                                num_of_rooms = f"5к+ {int(num_of_rooms.split('-')[0])}"
                            else:
                                num_of_rooms = f"{int(num_of_rooms.split('-')[0])}к"
                else:
                    print(value_of_field)

                    if re.search(r'общая', value_of_field[2]):
                        total_area = float(re.sub(r'[^0-9.]', '', value_of_field[0]))
                    if re.search(r'жилая', value_of_field[2]):
                        living_area = float(re.sub(r'[^0-9.]', '', value_of_field[0]))
                    if re.search(r'кухня', value_of_field[2]):
                        kitchen_area = float(re.sub(r'[^0-9.]', '', value_of_field[0]))
            phone_num = response.css(self.parsing_info_params['phone_num_selector']).get()
            phone_num = re.sub(r'[^0-9]', '', phone_num)
            item = {
                'mode': 1,
                'house_id': house_id,
                'type_of_participation': type_of_participation,
                'official_builder': official_builder,
                'name_of_build': name_of_build,
                'decoration': decoration,
                "floor": floor,
                "floor_count": floor_count,
                "house_type": house_type,
                "num_of_rooms": num_of_rooms,
                "total_area": total_area,
                "living_area": living_area,
                "kitchen_area": kitchen_area,
                'land_area': land_area,
                'data': data,
                'phone_num': phone_num,
                'img_set': images}
            yield item
        else:
            print('Too many views (>100)')
            delete_house_model(house_id)
