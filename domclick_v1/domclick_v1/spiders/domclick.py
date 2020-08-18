# -*- coding: utf-8 -*-
import os
import re
import sys
import scrapy
import requests as r
import json

cookie = {'PAINT_ACTIVE_MAP__COOKIE_VITRINA': '%7B%22value%22%3A2%7D',
          'ftgl_cookie_id': '758f2bd9b209fa84b09551be3653525a',
          'qrator_ssid': '1596657654.551.7k0gOZiOKTmCKiek-s4p6t60cvbp2fmr044r7h4dpnrkt547k',
          'RETENTION_COOKIES_NAME': '29b11b75cea24d9684c8529313af4e73:6_cOlskH-rmZ-jHToNDIH4nXy2Y',
          'sessionId': '98df7d68d10a4c61a73bcfd3c792a482:XOFCB3iVQJ3LQjyQOS4WYcj-amU',
          'UNIQ_SESSION_ID': '28d5026d91de482f902879e69453c9a2:P3JmjQd6bv9UWnVaBOz7bEswgDo',
          'auto-definition-region': 'false', '_sa': 'SA1.804e8be3-3667-46f6-9142-ad1e3d221a8d.1596657654',
          'SESSION': 'ba75fa55-4d77-44e5-87c4-128615acab4f',
          'region': '{%22data%22:{%22name%22:%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22%2C%22kladr%22:%2277%22%2C%22guid%22:%220c5b2444-70a0-4932-980c-b4dc0d3f02b5%22}%2C%22isAutoResolved%22:true}',
          'currentLocalityGuid': '9460fbc2-5e19-4fd2-bc0b-70a61bc1199c', 'currentSubDomain': 'tyumen',
          'regionName': '9460fbc2-5e19-4fd2-bc0b-70a61bc1199c:%D0%A2%D1%8E%D0%BC%D0%B5%D0%BD%D1%8C',
          'SLG_GWPT_Show_Hide_tmp': 1,
          'SLG_wptGlobTipTmp': 1,
          'mobile-region-shown': 1,
          'qrator_jsid': '1596657653.781.oqUsW7jmnBPMeRgR-j3tfo55v8mj5936i0fuiks4j34138o0u',
          'currentRegionGuid': 'dd883c15-4164-45c7-91fc-2a9381b5563b'
          }
DEBUG = True
if DEBUG:
    PATH_TO_DJANGO = '/Users/nikitatonkoskurov/PycharmProjects/domofound2'
else:
    PATH_TO_DJANGO = '/var/www/dom/src/'

sys.path.append(PATH_TO_DJANGO)
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from services import get_cord

from apps.base.models import HouseModel, CITY_CHOICES


def get_phone(house_id):
    try:
        a = r.get(url=f'https://offers-service.domclick.ru/research/v1/offers/phone/{house_id}')
        return a.json()['result']['phone']
    except:
        return '0'


def correct_house_id(url):
    house_id = re.sub(r'[^1-9]', '', re.sub(r'/|\?osale2|\?osale1| ', '', url))
    if len(house_id) > 10:
        return int(house_id) % 10000000
    else:
        return int(house_id)


def check_db(house_id_val):
    house = HouseModel.objects.filter(house_id=house_id_val)
    if house:
        return False
    else:
        return True


class DomclickSpider(scrapy.Spider):
    name = 'domclick'
    allowed_domains = ['tyumen.domclick.ru']
    start_urls = [
        'https://tyumen.domclick.ru/search/?category=living&deal_type=sale&from=topline2020&is_owner=1&ne=57.291641%2C65.776968&offer_type=flat&sw=56.982522%2C65.314855&sort=published&sort_dir=desc']
    urls_pool = [
        'https://tyumen.domclick.ru/search/?category=living&deal_type=sale&from=topline2020&is_owner=1&ne=57.291641%2C65.776968&offer_type=flat&sw=56.982522%2C65.314855&sort=published&sort_dir=desc']
    types = ['Новостройки', 'Вторичка', 'Коттеджи', 'Участки']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], headers={'Cookie': cookie}, callback=self.parse)

    def parse(self, response):
        cards = response.css('a._1X0Y9')
        page_index = self.urls_pool.index(response.url)
        for card in cards:
            if cards.index(card) < 3:
                link = response.urljoin(card.css('::attr(href)').get())
                house_id = correct_house_id(card.css('.layout-RNrDu medium-2Yzjc::attr(id)').get())
                print(link)
                if check_db(house_id):
                    pass
                    # yield self.parse_card(card, response, page_index)
                    # yield scrapy.Request(url=link, callback=self.parse_info)
                else:
                    print('THIS HOUSE ALREADY EXIST')
        if page_index < self.urls_pool.__len__() - 1:
            yield scrapy.Request(url=self.urls_pool[page_index + 1], callback=self.parse)
