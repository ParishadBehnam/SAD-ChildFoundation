from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'hamyar_register$', views.hamyar_register, name='hamyar_register'),
    url(r'login$', views.login, name='login'),
    url(r'', views.general_information, name='general_information'),
]
