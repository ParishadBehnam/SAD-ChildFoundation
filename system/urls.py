from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'show_madadjoo$', views.show_madadjoo, name='show_madadjoo'),
    url(r'', views.general_information, name='general_information'),
]
