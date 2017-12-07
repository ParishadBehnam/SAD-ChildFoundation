# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm

from system.models import information
from active_user.models import *

from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

class MyAdminSite(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('بنیاد کودک')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('بنیاد کودک')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('بنیاد کودک-پنل مدیریت')

admin_site = MyAdminSite()


class InformationAdmin(admin.ModelAdmin):
    list_display = ("history", "activities")

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = active_user
        #fields = ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address")


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ("first_name", "last_name")

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address",),
        }),
    )
class MadadkarAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ("first_name", "last_name")

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address", "bio",),
        }),
    )

class HamyarAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ("first_name", "last_name")

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address",),
        }),
    )

class MadadjooAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ("first_name", "last_name")

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address", "bio", "edu_status","successes", "invest_percentage"),
        }),
    )



admin_site.register(information, InformationAdmin)
admin_site.register(active_user, UserAdmin)
admin_site.register(madadkar, MadadkarAdmin)
admin_site.register(hamyar, HamyarAdmin)
admin_site.register(madadjoo, MadadjooAdmin)
