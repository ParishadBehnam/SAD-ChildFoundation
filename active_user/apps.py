# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ActiveUserConfig(AppConfig):
    name = 'active_user'
    verbose_name = 'کاربران فعال'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('active_user'))
        registry.register(self.get_model('madadjoo'))
        registry.register(self.get_model('madadkar'))
        registry.register(self.get_model('hamyar'))
        registry.register(self.get_model('admin_user'))
        registry.register(self.get_model('madadkar_remove_madadjoo'))
        registry.register(self.get_model('madadjoo_madadkar_letter'))
        registry.register(self.get_model('requirements'))
        registry.register(self.get_model('hamyar_system_payment'))
        registry.register(self.get_model('sponsership'))
        registry.register(self.get_model('hamyar_madadjoo_payment'))
        registry.register(self.get_model('hamyar_madadjoo_non_cash'))
        registry.register(self.get_model('hamyar_madadjoo_meeting'))
        registry.register(self.get_model('madadjoo_hamyar_letter'))
        registry.register(self.get_model('add_madadjoo_admin_letter'))
        registry.register(self.get_model('urgent_need_admin_letter'))
        registry.register(self.get_model('warning_admin_letter'))
