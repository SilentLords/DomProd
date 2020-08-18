import random
from django.utils import timezone
from django.contrib.auth import login
from knox.views import LoginView
from knox.models import AuthToken
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, permissions
from apps.users.serializers import CreateUserSerializer, LoginSerializer, UserSerializer
from .models import User, PhoneOTP, Payment
# from knox.views import LoginView
import requests
import re
from .payments import create_payment, check_payment

REFERRAL_VALUES = {
    'days': 7,
    'days_add_to_parent': 1,
    'hours_add_to_referral': 1,
    'partner_days_to_activate': 31,
    'discount_add_count': 2
}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


def correct_num(num):
    return re.sub(r'\+|-|\(|\)', '', num)


# Create your views here.
class ValidatePhone(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_num = correct_num(request.data.get('number'))
        if phone_num:
            phone = str(phone_num)
            user = User.objects.filter(phone__iexact=phone)
            if user:
                return Response({
                    'status': False,
                    'detail': 'Такой номер телефона уже существует'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old:
                        old = old.first()
                        print(old.count)
                        if old.count > 10:
                            return Response({
                                'status': False,
                                'detail': 'Отправка не выполнена. Привышен лимит сообщений обратитесь в тех поддержку'
                            })
                        old.otp = key
                        old.count += 1
                        old.save()
                        return Response({
                            'status': True,
                            'detail': 'Send is ok'
                        }, headers={'Access-Control-Allow-Origin': '*'})
                    else:
                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key

                        )
                        return Response({
                            'status': True,
                            'detail': 'СМС отправлено'
                        })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Отправка провалилась, проверте номер телефона и попробуйте еще раз'
                    })
        else:
            return Response({
                'status': False,
                'detail': 'Введите номер телефона'
            })


class ValidateOTP(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_num = correct_num(request.data.get('number', False))
        otp = request.data.get('code', False)
        print(phone_num)
        if phone_num and otp:
            old = PhoneOTP.objects.filter(phone__iexact=str(phone_num))
            if old:
                old = old.first()
                print(old.otp)
                if str(old.otp) == str(otp):
                    old.validate = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'Одноразовый код найден'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Не корректный код '
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Сначала отправте смс код'
                })
        else:
            return Response({

                'status': False,
                'detail': 'В запросе должен быть номер телефона и смс код '
            })


class Register(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        phone_num = correct_num(request.data.get('number'))
        email = request.data.get('email')
        password = request.data.get('password')
        ref_code = request.data.get('ref_code')
        is_referral = False
        if ref_code:
            is_referral = True
        if phone_num and email and password:
            old = PhoneOTP.objects.filter(phone__iexact=str(phone_num))
            if old:
                old = old.first()
                if old.validate:
                    temp_data = {
                        'phone': phone_num,
                        'email': email,
                        'password': password
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    if is_referral:
                        if User.objects.filter(referral_code=ref_code):
                            user.parent_referral = User.objects.get(referral_code=ref_code)
                            user.subscribe_hours_count += REFERRAL_VALUES['hours_add_to_referral']
                            user.subscribe_days_count += 1
                            user.save()
                        else:
                            pass
                    user.save()
                    # token = AuthToken.objects.get(user=user).token_key + AuthToken.objects.get(user=user).salt
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Пользователь создан!',
                        # 'token': token
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': "Смс код не подтвержден!"
                    })
            else:
                return Response({
                    'status': False,
                    'detail': "Сначала подтвердите номер телефона "
                })
        else:
            return Response({
                'status': False,
                'detail': "В запросе должен быть email, пароль, телефон "
            })


class SendResetOTP(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        phone = correct_num(request.data.get('number'))
        if phone:
            otp = send_reset_otp(phone)
            PhoneOTP.objects.create(otp=otp, phone=phone)
            return Response({
                'status': True,
                'detail': 'СМС код отправлен'
            })
        else:
            return Response({
                'status': False,
                'detail': 'В запросе должен быть телефон'
            })


class ValidateOTP(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        phone_num = correct_num(request.data.get('number', False))
        otp = request.data.get('code', False)
        if phone_num and otp:
            old = PhoneOTP.objects.filter(phone__iexact=str(phone_num))
            if old:
                old = old.first()
                print(old.otp)
                if str(old.otp) == str(otp):
                    old.validate = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'Одноразовый код найден'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'Не корректный код '
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'Сначала отправте смс код'
                })
        else:
            return Response({

                'status': False,
                'detail': 'В запросе должен быть номер телефона и смс код '
            })


class ResetPassword(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        phone_num = correct_num(request.data.get('number', False))
        password = request.data.get('password', False)
        if phone_num and password:
            user = User.objects.filter(phone=phone_num)
            if user:
                user[0].password = password
                user[0].save()
                if AuthToken.objects.filter(user__phone=user[0].phone):
                    AuthToken.objects.filter(user__phone=user[0].phone).delete()
                PhoneOTP.objects.filter(phone=user[0].phone).delete()
                return Response({
                    'status': False,
                    'detail': 'Пароль изменен'
                })
            else:
                return Response({

                    'status': False,
                    'detail': 'Пользователь с таким номером телефона не найден'
                })
        else:
            return Response({

                'status': False,
                'detail': 'В запросе должен быть номер телефона и пароль '
            })


def send_otp(phone):
    if phone:
        print(phone)
        code = random.randint(999, 9999)
        print(code)
        requests.post(
            f'https://sms.ru/sms/send?api_id=7A4D03D4-8154-FF98-E7AB-413BF7496EF6&to={phone},&msg={code}&json=1')
        return code
    else:
        return False


def send_reset_otp(phone):
    if phone:
        print(phone)
        code = random.randint(9999, 99999)
        print(code)
        # if settings.DEBUG:
        #     return code
        # else:
        requests.post(
            f'https://sms.ru/sms/send?api_id=7A4D03D4-8154-FF98-E7AB-413BF7496EF6&to={phone},&msg={code}&json=1')
        # print(requests)
        return code
    else:
        return False


class LoginAPI(LoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # print(1)
        # print(user)
        login(request, user)
        # request.data.update({'status': True})
        return super().post(request, format=None)

def get_online_users_count():
    ago5m = timezone.now() - timezone.timedelta(minutes=5)
    count = User.objects.filter(last_login__gte=ago5m).count()
    return count
class UserView(RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    model = User
    serializer_class = UserSerializer

    def retrieve(self, request):
        """
        If provided 'pk' is "me" then return the current user.
        """
        payments_count = 0
        payments = Payment.objects.filter(user=UserSerializer(request.user).data['id'], is_success=False)
        if payments:
            payments_count = 0
            for payment in payments:
                payments_count = check_and_complite_payment(payment, payments_count, User.objects.get(
                    id=UserSerializer(request.user).data['id']))
                payments_count += 1
        print(payments_count)
        if request.user:
            return Response({'user': UserSerializer(request.user).data, 'online_count': get_online_users_count()})
        return super(UserView, self).retrieve(request)


class CreatePayment(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_id = UserSerializer(request.user).data['id']
        user = User.objects.get(id=user_id)
        days = int(request.data['days'])
        price = int(request.data['price'])
        price_with_discount = price - (user.all_discount_count * 0.01) * price
        url, p_id = create_payment(price_with_discount, days)
        Payment.objects.create(user=user, payment_id=p_id, days=days)
        return Response({'status': True, 'url': url})


class PaymentSuccess(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user_id = UserSerializer(request.user).data['id']
        user = User.objects.get(id=user_id)
        payments = Payment.objects.filter(user=user, is_success=False)
        if payments:
            payments_count = 0
            for payment in payments:
                payments_count = check_and_complite_payment(payment, payments_count, user)
                payments_count += 1
                if payments_count > 0:
                    return Response({'status': True, 'payments_count': payments_count})
                else:
                    return Response({'status': False})
            else:
                return Response({'status': False})
        else:
            return Response({'status': False})


def check_and_complite_payment(payment, payments_count, user):
    if check_payment(payment.payment_id):
        days = payment.days

        if user.parent_referral:
            if not user.is_partner:
                if days == REFERRAL_VALUES['partner_days_to_activate']:
                    parent = user.parent_referral
                    parent.all_discount_count += REFERRAL_VALUES['discount_add_count']
                    print(parent.all_discount_count)
                    parent.save()
        if not user.is_partner:
            if days == REFERRAL_VALUES['partner_days_to_activate']:
                user.is_partner = True
                user.referral_code = random.randint(9999, 999999)
                user.save()
        user.subscribe_days_count += days
        user.is_subscribe = True
        user.save()
        payment.is_success = True
        payment.save()
    return payments_count
