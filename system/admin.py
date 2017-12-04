# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm

from system.models import information
from active_user.models import active_user


class InformationAdmin(admin.ModelAdmin):
    list_display = ("history", "activities")

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = active_user
        fields = ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address")


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ("first_name", "last_name")

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ("username", "password", "first_name", "last_name", "id_number", "phone_number", "address",),
        }),
    )


admin.site.register(information, InformationAdmin)
admin.site.register(active_user, UserAdmin)
