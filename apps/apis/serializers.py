from abc import ABC

from apps.users.models import User
from rest_framework import serializers
from .models import HouseModel, HouseInfo


class HouseInfo(serializers.ModelSerializer):
    class Meta():
        model = HouseInfo
        field = ('__all__')


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseModel
        fields = ("__all__")


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


class AdvancedHouseSerializer(serializers.Serializer):
    def validate(self, data):
        houses = []
        user_id = UserSerializer(data.user).data['id']
        for house in HouseModel.objects.all():
            if house.ignore_list.filter(id=user_id).exists():
                print('find ignore house')
            elif house.fav_list.filter(id=user_id).exists() and not house.watched_list.filter(id=user_id).exists():
                houses.append({"items": HouseSerializer(house, many=False).data, 'is_fav': True, 'is_watched': False})
            elif house.watched_list.filter(id=user_id).exists() and not house.fav_list.filter(id=user_id).exists():
                houses.append({"items": HouseSerializer(house, many=False).data, 'is_fav': False, 'is_watched': True})
            elif house.watched_list.filter(id=user_id).exists() and house.fav_list.filter(id=user_id).exists():
                houses.append({"items": HouseSerializer(house, many=False).data, 'is_fav': True, 'is_watched': True})
            else:
                houses.append({"items": HouseSerializer(house, many=False).data, 'is_fav': False, 'is_watched': False})
        # print(houses)
        return houses
