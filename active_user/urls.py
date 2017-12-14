from django.conf.urls import url
from active_user import views

urlpatterns = [
    url(r'show_madadjoo$', views.show_madadjoo, name='show_madadjoo'),
    url(r'edit_madadjoo$', views.edit_madadjoo, name='edit_madadjoo'),
    url(r'add_madadjoo', views.add_madadjoo, name='add_madadjoo'),
    url(r'show_a_madadjoo$', views.show_a_madadjoo, name='show_a_madadjoo'),
    url(r'show_a_hamyar$', views.show_a_hamyar, name='show_a_hamyar'),
    url(r'send_letter$', views.send_letter, name='send_letter'),
    url(r'inbox$', views.inbox, name='inbox'),
    url(r'madadkar_panel$', views.madadkar_panel, name='madadkar_panel'),
]
