# import time
#
# from django.shortcuts import render
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from requests import status_codes
# from rest_framework.utils import json
# from rest_framework.views import APIView
#
# from apps.users.models import User
# from .serializers import HouseSerializer, AdvancedHouseSerializer, UserSerializer, UserIgnore, UserWatch, UserFav
# from .models import HouseModel
# from .utils import reparse
# from corsheaders import check_settings
# from django.conf import settings
#
# check_settings(settings)
#
#
# def get_user_and_house(request):
#     user_id = UserSerializer(request.user).data['id']
#     user = User.objects.get(id=user_id)
#     house = HouseModel.objects.filter(id=request.data['house_id'])
#     return house, user
#
#
# # Create your views here.
# class Reparse(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         reparse()
#         houses = HouseModel.objects.all()
#         serializer = HouseSerializer(houses, many=True)
#         return Response(serializer.data)
#
#
# class GetBase(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     """Возвращает список домов"""
#
#     def get(self, request):
#         house = HouseModel.objects.filter()
#         # print(house.)
#         serializer = HouseSerializer(house, many=True)
#         print(serializer.data)
#         return Response(serializer.data)
#
#
# class House(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, pk):
#         house = HouseModel.objects.get(id=pk)
#         serializer = HouseSerializer(house, many=False)
#         print(serializer.data)
#         return Response(serializer.data)
#
#
# class HouseAdvanced(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         # t0 = time.time()
#         serializer = AdvancedHouseSerializer(data=request)
#         data = serializer.validate(request)
#         # print(time.time() - t0)
#         return Response({'status': True, 'data': data})
#
#
# class IgnoreList(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.ignore_list.add(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success add to ignore list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#     def delete(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.ignore_list.remove(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success add to ignore list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#
# class WatchList(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.watched_list.add(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success add to watch list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#     def delete(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.watched_list.remove(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success remove from watch list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#
# class FavList(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.fav_list.add(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success add to favorite list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#     def delete(self, request):
#         house, user = get_user_and_house(request)
#         if house.exists():
#             user.fav_list.remove(house[0])
#             user.save()
#             return Response({'status': True, 'detail': 'Success remove from favorite list'})
#         else:
#             Response({'status': False, 'detail': 'House with this id did not find'})
#
#
# class GetIgnore(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         print(UserIgnore(request.user).data)
#         return Response({'items': UserIgnore(request.user).data, 'status': True})
#
#
# class GetFav(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         print(UserFav(request.user).data)
#         return Response({'items': UserIgnore(request.user).data, 'status': True})
#
#
# class GetWatch(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request):
#         print(UserWatch(request.user).data)
#         return Response({'items': UserIgnore(request.user).data, 'status': True})
