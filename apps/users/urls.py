from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
from knox.views import LogoutView
from .views import ValidatePhone, ValidateOTP, Register, LoginAPI, UserView, PaymentSuccess, CreatePayment, \
    ResetPassword, SendResetOTP

# from rest_framework.authtoken.views import obtain_auth_token

#


urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('reset/find_phone/', SendResetOTP.as_view()),
    path('reset/validate_otp/', ValidateOTP.as_view()),
    path('reset/change_password/', ResetPassword.as_view()),
    path('login/', LoginAPI.as_view()),
    path('logout/', LogoutView.as_view()),
    path('me/', UserView.as_view()),
    path('registration/validate_phone/', ValidatePhone.as_view()),
    path('registration/validate_otp/', ValidateOTP.as_view()),
    path('registration/me/', Register.as_view()),
    path('payments/success/', PaymentSuccess.as_view()),
    path('payments/create/', CreatePayment.as_view()),
]
