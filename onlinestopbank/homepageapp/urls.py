from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import Index, Registration, Login, RegisterSuccess, Main, ProfileAccount, logout, deposit, withdraw, bill_payment, payment_failed, payment_success, transfer, Update_Account, Updated


urlpatterns = [
    path('', Index, name="home"),
    path('login', Login, name="login"),
    path('logout', logout, name="logout"),
    path('registration', Registration, name="registration"),
    path('registersuccess', RegisterSuccess, name="registersuccess"),
    path('main', Main, name="main"),
    path('account', ProfileAccount, name="account"),
    path('deposite', deposit, name="deposite"),
    path('withdraw', withdraw, name="withdraw"),
    path('billpayment', bill_payment, name="billpayment"),
    path('payment_success',payment_success,name='payment_success'),
    path('payment_failed',payment_failed,name='payment_failed'),
    path('transfer', transfer, name="transfer"),
    path('updateprofile', Update_Account, name="updateprofile"),
    path('updated', Updated, name="updated"),


]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)