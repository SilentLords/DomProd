# -*- coding: utf-8 -*-
import csv
import os
import re
import sqlite3
import sys
from .services import get_cord
import scrapy

DEBUG = False
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()


def correct_price(text):
    return re.sub(r'\n|₽| ', '', text)


from apps.base.models import HouseModel, CITY_CHOICES


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    link_pool = []
    urls_pool = ['https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1',
                 'https://www.avito.ru/tyumen/doma_dachi_kottedzhi/prodam/kottedzh-ASgBAgICAkSUA9AQ2AjKWQ',
                 'https://www.avito.ru/tyumen/zemelnye_uchastki/prodam-ASgBAgICAUSWA9oQ']
    start_urls = ['https://www.avito.ru/tyumen/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1']

    def parse(self, response):
        city = 0
        page_index = self.urls_pool.index(response.url)
        print("processing: " + response.url)
        products = response.css('.item__line')
        i = 0
        ob_params = {
            'max_ob': 5
        }
        for item in products:
            if i <= ob_params['max_ob']:
                data = ''
                if item.css('span.item-address-georeferences').get():
                    geo = item.css(
                        'span.item-address-georeferences-item__content::text').get()
                else:
                    geo = ''
                if item.css('a.snippet-link::attr(href)').get().split("._").__len__() > 2:
                    h_id = re.sub(r'[^0-9]', '', item.css('a.snippet-link::attr(href)').get().split("._")[2])
                else:
                    print(item.css('a.snippet-link::attr(href)').get().split("._"))
                    if item.css('a.snippet-link::attr(href)').get().split("._").__len__() == 1:
                        h_id = re.sub(r'[^0-9]', '', item.css('a.snippet-link::attr(href)').get().split("_")[-1])
                    else:
                        h_id = re.sub(r'[^0-9]', '', item.css('a.snippet-link::attr(href)').get().split("._")[1])
                if self.check_db(h_id):
                    self.link_pool.append(response.urljoin(item.css('a.snippet-link::attr(href)').get()))
                print(page_index)
                if 0 <= page_index < 3:
                    city = 0
                else:
                    city = 0
                full_address = CITY_CHOICES[city][1] + item.css('span.item-address__string::text').get() + ' ' + geo
                y_cord, x_cord = get_cord(address=full_address)
                print(item.css('h3.snippet-title >a > span::text').get())
                yield {
                    'house_id': h_id,
                    'img': item.css('img.large-picture-img::attr(src)').get(),
                    'title': item.css('h3.snippet-title >a > span::text').get(),
                    'link': response.urljoin(item.css('h3.snippet-title > a.snippet-link::attr(href)').get()),
                    'price': int(correct_price(item.css('span.snippet-price::text').get())),
                    'address': full_address,
                    'data': data,
                    'time_created': item.css('div.snippet-date-info::text').get(),
                    'host': self.allowed_domains[0],
                    'city': city,
                    'cords': [x_cord, y_cord]
                }
                i += 1
        print(page_index)
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(self.urls_pool[page_index + 1], callback=self.parse)
        else:
            self.save()

    def check_db(self, house_id_val):
        house = HouseModel.objects.filter(house_id=house_id_val)
        if house:
            return False
        else:
            return True

    def save(self):
        # print('save', self.link_pool)
        with open('../../../info/info/spiders/links.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for link in self.link_pool:
                writer.writerow([link])
