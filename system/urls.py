from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'show_madadjoo$', views.show_madadjoo, name='show_madadjoo'),
    url(r'edit_madadjoo$', views.edit_madadjoo, name='edit_madadjoo'),
    url(r'show_a_madadjoo$', views.show_a_madadjoo, name='show_a_madadjoo'),
    url(r'show_a_hamyar$', views.show_a_hamyar, name='show_a_hamyar'),
    url(r'send_letter$', views.send_letter, name='send_letter'),
    url(r'madadkar_panel$', views.madadkar_panel, name='madadkar_panel'),
    url(r'hamyar_register$', views.hamyar_register, name='hamyar_register'),
    url(r'login$', views.login, name='login'),
    url(r'', views.general_information, name='general_information'),
]
