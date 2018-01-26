from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    url(r'^hamyar_register$', views.hamyar_register, name='hamyar_register'),
    url(r'^login$', views.sign_in, name='login'),
    url(r'^logout', views.system_logout, name='system_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'', views.general_information, name='general_information'),
]
