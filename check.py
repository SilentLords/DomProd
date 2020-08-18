#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

sys.path.append('/Users/nikitatonkoskurov/PycharmProjects/domofound2/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'domofound2.settings'
import django

django.setup()
from apps.users.models import User


def check_subscribe_time():
    users = User.objects.exclude(is_subscribe=False)
    print(users)
    for user in users:
        ##Более менее нормальный код
        print(f'Start check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}')
        user.subscribe_hours_count -= 1
        if user.subscribe_hours_count == 0:
            if user.subscribe_days_count == 0:
                user.is_subscribe = False
                user.subscribe_days_count = 0
                user.subscribe_hours_count = 0
                user.save()
            else:
                user.subscribe_days_count -= 1
                user.subscribe_hours_count = 24
                user.save()
        user.save()
        print(f'End check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, is_subscribe: {user.is_subscribe}')

        #####Памятник моему идиотизму!!

        # first_check = False
        # if user.subscribe_days_count >= 1 and user.subscribe_hours_count >= 1:
        #     user.subscribe_hours_count -= 1
        #     user.save()
        #     if user.subscribe_hours_count == 0 and user.subscribe_days_count > 0:
        #         user.subscribe_days_count -= 1
        #         user.subscribe_hours_count = 24
        #         user.save()
        #     first_check = True
        #     print(
        #     f'Start 1 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')
        #
        # if user.subscribe_days_count == 0 and user.subscribe_hours_count > 0 and not first_check:
        #     user.subscribe_hours_count -= 1
        #     user.save()
        #     print(
        #     f'Start 2 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')
        #
        # if user.subscribe_days_count == 0 and user.subscribe_hours_count == 0:
        #     user.subscribe_days_count = 0
        #     user.subscribe_hours_count = 0
        #     user.is_subscribe = False
        #     user.save()
        #     print(
        #     f'Start 3 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')


if __name__ == "__main__":
    check_subscribe_time()
