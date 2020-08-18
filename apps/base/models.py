from django.db import models
from django.db.models import CASCADE

CITY_CHOICES = ((0, 'Тюмень'),)
OFFER_CHOICES = ((0, 'Купить'), (1, "Аренда"))
import datetime


class HouseInfo(models.Model):
    house_id = models.IntegerField(default=0, verbose_name='house_id')
    type_of_participation = models.CharField(max_length=20, default='')
    official_builder = models.CharField(max_length=20, default='')
    name_of_build = models.CharField(max_length=20, default='')
    decoration = models.CharField(max_length=20, default='')
    floor = models.IntegerField(default=0)
    floor_count = models.IntegerField(default=0)
    house_type = models.CharField(max_length=20, default='')
    num_of_rooms = models.CharField(max_length=20, default='')
    total_area = models.FloatField(default=0)
    living_area = models.FloatField(default=0)
    kitchen_area = models.FloatField(default=0)
    deadline = models.CharField(max_length=20, default='')
    phone = models.IntegerField(default=0)
    land_area = models.FloatField(default=0)

    def __str__(self):
        return f'ID: {str(self.id)} PHONE: {str(self.phone)} HOUSE_ID: {str(self.house_id)}'


# Create your models here.
class HouseModel(models.Model):
    offer_type = models.CharField(choices=OFFER_CHOICES, max_length=40, default=0)
    type = models.CharField(max_length=20, null=True, blank=True)
    house_id = models.IntegerField(default=0, verbose_name='house_id')
    title = models.CharField(verbose_name="Title", name="title", max_length=200)
    title_image = models.CharField(max_length=300, verbose_name='Title Image', blank=True, null=True)
    link = models.URLField(verbose_name="Link", name="link", max_length=200)
    price = models.FloatField(verbose_name="Price", name="price", default=0)
    address = models.CharField(verbose_name="Address", name="address", max_length=200)
    data = models.TextField(verbose_name="Data", name="data", null=True, blank=True)
    time_to_create = models.CharField(verbose_name="Time", name="time", max_length=200, blank=True)
    host = models.CharField(verbose_name="Host", name="Host", max_length=200, )
    house_info = models.ForeignKey(HouseInfo, on_delete=CASCADE, null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITY_CHOICES, null=True, blank=True)
    x_cord = models.FloatField(null=True, blank=True)
    y_cord = models.FloatField(null=True, blank=True)
    parsing_time = models.DateTimeField(auto_now_add=True, verbose_name="creation_time")
    ready_to_go = models.BooleanField(default=True, verbose_name="ready_to_go")

    def __str__(self):
        return "ID: " + str(self.id) + ", host: " + str(self.Host) + ', House_id: ' + str(self.house_id)


class Image(models.Model):
    house = models.ForeignKey(HouseModel, on_delete=CASCADE)
    image_link = models.CharField(verbose_name='photo', max_length=1000)

    def __str__(self):
        return str(self.id) + str(self.house)
# Create your models here.
