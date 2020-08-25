import time

DEBUG = False
from django.utils import timezone
from apps.users.models import User
from rest_framework import serializers
from .models import HouseModel, HouseInfo, Image

#
if not DEBUG:
    from shapely.geometry import Point
    from shapely.geometry.polygon import Polygon
import random
import time

#
if not DEBUG:
    def check_cords(polygon_cords, houses_query):
        print(type(polygon_cords))
        finish_poligon_cords = []
        for i in polygon_cords:
            finish_poligon_cords.append((i[0], i[1]))
        print(finish_poligon_cords)
        polygon = Polygon(finish_poligon_cords)
        print(polygon)
        print(polygon.is_valid)
        result_list = []
        for house in houses_query:
            if house.x_cord and house.y_cord:
                point = Point(house.x_cord, house.y_cord)
                if polygon.contains(point):
                    result_list.append(house)
        print(result_list)
        return result_list


class HouseInfo(serializers.ModelSerializer):
    class Meta():
        model = HouseInfo
        fields = '__all__'


# Polygon([(30, 30), (30, 90), (90, 90), (90,30)])
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_link',)


class HouseSerializer(serializers.ModelSerializer):
    image_set = ImageSerializer(many=True)
    house_info = HouseInfo(many=False)

    class Meta:
        model = HouseModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # fav_list = HouseSerializer(many=True)
    # ignore_list = HouseSerializer(many=True)
    # watched_list = HouseSerializer(many=True)

    class Meta:
        model = User
        fields = ('id',)


class UserIgnore(serializers.ModelSerializer):
    # fav_list = HouseSerializer(many=True)
    ignore_list = HouseSerializer(many=True)

    # watched_list = HouseSerializer(many=True)

    class Meta:
        model = User
        fields = ('ignore_list',)


class UserWatch(serializers.ModelSerializer):
    # fav_list = HouseSerializer(many=True)
    # ignore_list = HouseSerializer(many=True)
    watched_list = HouseSerializer(many=True)

    class Meta:
        model = User
        fields = ('watched_list',)


class UserFav(serializers.ModelSerializer):
    fav_list = HouseSerializer(many=True)

    # ignore_list = HouseSerializer(many=True)
    # watched_list = HouseSerializer(many=True)

    class Meta:
        model = User
        fields = ('fav_list',)


class IgnoreSerializer(serializers.Serializer):
    def validate(self, data, polygon_cords=None):
        user_id = UserSerializer(data.user).data['id']
        houses = HouseModel.objects.exclude(ignore_list=user_id).order_by('-id').filter(ready_to_go=True)
        if not DEBUG:
            if polygon_cords:
                finish_list = check_cords(polygon_cords=polygon_cords, houses_query=houses)
                id_list = []
                for house in finish_list:
                    id_list.append(house.id)
                houses = HouseModel.objects.filter(pk__in=id_list).order_by('-id').filter(ready_to_go=True)
        if data['days_ago'] != 0:
            id_list = []
            for house in houses:
                id_list.append(house.id)
            ago_days = timezone.now() - timezone.timedelta(days=data['days_ago'])
            houses = HouseModel.objects.filter(pk__in=id_list).filter(parsing_time__gte=ago_days).order_by('-id')
        return houses


def get_online_users_count():
    ago5m = timezone.now() - timezone.timedelta(minutes=5)
    count = User.objects.filter(last_login__gte=ago5m).count()
    return count


class AdvancedHouseSerializer(serializers.Serializer):

    def validate(self, data, queryset):
        houses = []
        all_houses = queryset
        # print(all_houses)
        user_id = UserSerializer(data.user).data['id']
        t1 = time.time()
        for house in all_houses:
            if house.house_info:
                phone = house.house_info.phone
            else:
                phone = 0
            houses.append({"items": {'offer_type': house.offer_type, 'id': house.id, 'title': house.title,
                                     'address': house.address,
                                     'phone': phone, 'image_link': house.title_image,
                                     'host': house.Host,
                                     'link': house.link,
                                     'price': house.price,
                                     'time': house.parsing_time, 'ready_to_go': house.ready_to_go},
                           'is_fav': house.fav_list.filter(id=user_id).exists(),
                           'is_watched': house.watched_list.filter(id=user_id).exists()})
        t2 = time.time()
        print(f'------Time:{-t1 + t2}------')
        return houses
