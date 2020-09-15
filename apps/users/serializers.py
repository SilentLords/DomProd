from knox.models import AuthToken
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
import re
from apps.base.serializers import HouseSerializer

User = get_user_model()


def correct_num(num):
    return re.sub(r'\+|-|\(|\)', '', num)


def authenticate(username=None, password=None, **kwargs):
    from django.contrib.auth import get_user_model
    UserModel = get_user_model()
    if username is None:
        # print('there')
        username = kwargs.get(UserModel.USERNAME_FIELD)
    try:
        # print('there1')
        user = UserModel._default_manager.get_by_natural_key(username)
        # print(user.get_username())
        # print(user.password,password)
        # print(user.check_password(password))
        if user.admin:
            if user.check_password(str(password)):
                # print('pass')
                return user
        else:
            if user.password == password:
                # print('Base user login')
                return user
    except UserModel.DoesNotExist:
        # Run the default password hasher once to reduce the timing
        # difference between an existing and a non-existing user (#20760).
        UserModel().set_password(password)


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.is_subscribe = True
        user.subscribe_hours_count = 3
        user.save()
        # AuthToken.objects.create(user)
        return user


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'subscribe_days_count')


class UserSerializer(serializers.ModelSerializer):
    fav_list = HouseSerializer(many=True)
    ignore_list = HouseSerializer(many=True)
    watched_list = HouseSerializer(many=True)
    user_set = ReferralSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone', 'email', 'is_subscribe', 'subscribe_days_count', 'watched_list', 'fav_list', 'ignore_list',
            'subscribe_hours_count', 'is_partner', 'user_set', 'referral_code', 'commission_percentage',
            'commission_surcharge')


#
class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, data):
        phone = correct_num(data.get('phone'))
        password = data.get('password')
        # print(phone, password)
        if phone and password:
            if User.objects.filter(phone=phone):
                # print(phone, password)
                user = authenticate(request=self.context.get('request'), phone=phone, password=password)
                # print(user)

            else:
                msg = {
                    'detail': 'Номер телефона или пароль не найдены. Попробуйте еще раз',
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail': 'Номер телефона или пароль не найдены. Попробуйте еще раз',
                    'status': False
                }
                raise serializers.ValidationError(msg)
        else:
            msg = {
                'detail': 'Введите номер телефона и пароль',
                'status': False
            }
            raise serializers.ValidationError(msg)
        data['user'] = user
        return data
