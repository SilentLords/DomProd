from .models import User

def check_subscribe_time():
    users = User.objects.exclude(is_subscribe=False)
    print(users)
    for user in users:
        print(
            f'Start check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}')

        if user.subscribe_days_count >= 1 and user.subscribe_hours_count >= 1:
            user.subscribe_hours_count -= 1
            user.save()
            if user.subscribe_hours_count == 0:
                user.subscribe_days_count -= 1
                user.subscribe_hours_count = 24
                user.save()
            print(
            f'Start 1 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')

        if user.subscribe_days_count == 0 and user.subscribe_hours_count > 0:
            user.subscribe_hours_count -= 1
            user.save()
            print(
            f'Start 2 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')

        if user.subscribe_days_count == 0 and user.subscribe_hours_count == 0:
            user.subscribe_days_count = 0
            user.subscribe_hours_count = 0
            user.is_subscribe = False
            user.save()
            print(
            f'Start 3 check with user: {user.phone}, days: {user.subscribe_days_count}, hours: {user.subscribe_hours_count}, subscribe: {user.is_subscribe}')

