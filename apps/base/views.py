from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import get_jkh_info
from apps.users.models import User
from .serializers import HouseSerializer, AdvancedHouseSerializer, UserSerializer, UserIgnore, UserWatch, UserFav, \
    IgnoreSerializer
from .models import HouseModel
from apps.base.utils import reparse
from corsheaders import check_settings
from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

check_settings(settings)

CHOICES = (('1к', '1к'), ('2к', '2к'), ('3к', '3к'), ('4к', '4к'), ('5к', '5к+'), ('студии', 'студии'))
CHOICES_TYPE = (('Вторичка', 'Вторичка'), ('Новостройки', 'Новостройки'), ('Коттеджи', "Коттеджи"),('Участки', 'Участки'))


class InfoFilters(filters.FilterSet):
    phone = filters.NumberFilter(field_name='house_info__phone', lookup_expr='iexact')
    id = filters.NumberFilter(field_name='house_info__house_id', lookup_expr='iexact')
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    num_of_rooms = filters.MultipleChoiceFilter(choices=CHOICES, field_name='house_info__num_of_rooms',
                                                lookup_expr='icontains', )
    street = filters.CharFilter(field_name='address', lookup_expr='icontains')
    type_house = filters.MultipleChoiceFilter(choices = CHOICES_TYPE ,field_name='type', lookup_expr='icontains',)
    max_floor = filters.NumberFilter(field_name='house_info__floor', lookup_expr='lte')
    min_floor = filters.NumberFilter(field_name='house_info__floor', lookup_expr='gte')
    max_floor_count = filters.NumberFilter(field_name='house_info__floor_count', lookup_expr='lte')
    min_floor_count = filters.NumberFilter(field_name='house_info__floor_count', lookup_expr='gte')
    min_area = filters.NumberFilter(field_name='house_info__total_area', lookup_expr='gte')
    max_area = filters.NumberFilter(field_name='house_info__total_area', lookup_expr='lte')
    min_kitchen_area = filters.NumberFilter(field_name='house_info__kitchen_area', lookup_expr='gte')
    max_kitchen_area = filters.NumberFilter(field_name='house_info__kitchen_area', lookup_expr='lte')
    min_living_area = filters.NumberFilter(field_name='house_info__living_area', lookup_expr='gte')
    max_living_area = filters.NumberFilter(field_name='house_info__living_area', lookup_expr='lte')
    min_land_area = filters.NumberFilter(field_name='house_info__land_area', lookup_expr='gte')
    max_land_area = filters.NumberFilter(field_name='house_info__land_area', lookup_expr='lte')

    class Meta:
        model = HouseModel
        fields = ['min_price','street', 'max_price', 'num_of_rooms', 'max_floor', 'min_floor', 'min_area', 'max_area',
                  'max_floor_count', 'min_floor_count', 'id', 'phone', 'type_house', 'min_kitchen_area',
                  'max_kitchen_area', 'min_living_area', 'max_living_area', 'min_land_area', 'max_land_area']


class Pagination(PageNumberPagination):
    page_size = 15

    def __init__(self, p):
        self.page_size = p


def get_user_and_house(request):
    user_id = UserSerializer(request.user).data['id']
    user = User.objects.get(id=user_id)
    house = HouseModel.objects.filter(id=request.data['house_id'])
    return house, user


# Create your views here.
class Reparse(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        reparse()
        houses = HouseModel.objects.all()
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data)


class GetBase(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    """Возвращает список домов"""

    def get(self, request):
        house = HouseModel.objects.filter()
        # print(house.)
        serializer = HouseSerializer(house, many=True)
        print(serializer.data)
        return Response(serializer.data)


class House(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        house = HouseModel.objects.get(id=pk)
        user_id = UserSerializer(request.user).data['id']
        serializer = HouseSerializer(house, many=False)
        return Response({'house': serializer.data, 'is_fav': house.fav_list.filter(id=user_id).exists(),
                         'is_watch': house.watched_list.filter(id=user_id).exists()})


class Gkh(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        house = HouseModel.objects.get(id=pk)
        data = get_jkh_info(house.address)
        return Response({'status': True, 'data': data})


class HouseAdvanced(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get(self, request, page_size):
        paginator = Pagination(page_size)
        query_set = HouseModel.objects.all()
        query_set = query_set.order_by('-id')
        request._full_data = {'houses': query_set}
        ignore_ser = IgnoreSerializer(data=request)
        request.data.update({'houses': ignore_ser.validate(request)})
        context = paginator.paginate_queryset(request.data['houses'], request)
        request.data.update({'houses': context})
        serializer = AdvancedHouseSerializer(data=request)
        data = serializer.validate(request)
        return paginator.get_paginated_response(data)


#

class IgnoreList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.ignore_list.add(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success add to ignore list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})

    def delete(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.ignore_list.remove(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success add to ignore list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})


class WatchList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.watched_list.add(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success add to watch list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})

    def delete(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.watched_list.remove(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success remove from watch list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})


class FavList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.fav_list.add(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success add to favorite list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})

    def delete(self, request):
        house, user = get_user_and_house(request)
        if house.exists():
            user.fav_list.remove(house[0])
            user.save()
            return Response({'status': True, 'detail': 'Success remove from favorite list'})
        else:
            Response({'status': False, 'detail': 'House with this id did not find'})


class GetIgnore(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({'items': UserIgnore(request.user).data, 'status': True})


class GetFav(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({'items': UserFav(request.user).data, 'status': True})


class GetWatch(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({'items': UserWatch(request.user).data, 'status': True})


class HouseListView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AdvancedHouseSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InfoFilters

    def get_queryset(self):
        ignore_ser = IgnoreSerializer(data=self.request)
        if self.request.data['polygon_cords'] != 0:
            queryset = ignore_ser.validate(data=self.request, polygon_cords=self.request.data['polygon_cords'])
        else:
            queryset = ignore_ser.validate(data=self.request)
        return queryset

    def list(self, request, page_size, *args, **kwargs):
        paginator = Pagination(page_size)
        queryset = self.filter_queryset(self.get_queryset())
        context = paginator.paginate_queryset(queryset, request)

        serializer = AdvancedHouseSerializer(self.request)
        final_context = serializer.validate(self.request, context)
        return paginator.get_paginated_response(final_context)

    def post(self, request, *args, **kwargs):
        page_size = request.data['page_size']
        return self.list(request, page_size)


class GetListOfStreets(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        with open('tymen_streets.txt', 'r') as f:
            streets = f.readlines()
        return Response({'status': True, "list": streets})