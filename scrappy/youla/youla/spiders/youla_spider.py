# -*- coding: utf-8 -*-
import csv
import sqlite3

import scrapy
import re


class YoulaSpiderSpider(scrapy.Spider):
    name = 'youla_spider'
    link_pool = []
    allowed_domains = ['youla.ru']
    start_urls = ['https://youla.ru/tyumen/nedvijimost/prodaja-kvartiri?attributes[sort_field]=date_published']

    def parse(self, response):
        print("processing: " + response.url)
        product_cards = response.css('li.product_item')
        # print(product_cards)
        for product in product_cards:
            if product.css('.product_item--promoted'):
                print('Its promoted')
            else:
                print(response.urljoin(product.css('a::attr(href)').get()))
                print(re.sub('[^0-9]', '', product.css('a::attr(href)').get().split('-')[-1]))
                print(product.css('.product_item__title::text').get())
                print(product.css('.product_item__description >  div::text').get().replace(' ', '').replace('\n', ''))
                print(product.css('span.product_item__location::text').get().replace(' ', '').replace('\n', ''))
                print(product.css('svg#svg_1 > image').get().split('xlink:href="')[1].split('"')[0])
                print(product.css('span.visible-xs::text').get())
                if self.check_db(re.sub('[^0-9]', '', product.css('a::attr(href)').get().split('-')[-1])):
                    self.link_pool.append(response.urljoin(product.css('a::attr(href)').get()))
        # print(self.link_pool)
        self.save()

    def check_db(self, house_id_val):
        conn = sqlite3.connect('/Users/nikitatonkoskurov/PycharmProjects/domofound2/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT house_id FROM base_housemodel WHERE house_id=?', (house_id_val,))
        a = cursor.fetchone()
        # print(a)
        if a:
            return False
        else:
            return True

    def save(self):
        # print('save', self.link_pool)
        with open('../../info/info/spiders/links.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for link in self.link_pool:
                writer.writerow([link])
