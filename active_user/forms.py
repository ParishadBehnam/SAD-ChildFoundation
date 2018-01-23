# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate
from django.forms import ModelForm, forms
from django import forms
from active_user import models
from active_user.models import hamyar
from django.utils.translation import ugettext_lazy as _


class hamyar_form(ModelForm):
    class Meta:
        model = models.hamyar
        fields = ['username', 'password', 'first_name', 'last_name', 'id_number', 'phone_number', 'email', 'address']
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }

        error_messages = {
            'username': {
                'unique': _("این نام کاربری قبلا انتخاب شده است."),
            },
            'id_number': {
                'unique': _("این کد ملی در سیستم ثبت شده است."),
            },
        }

    def clean(self):
        cleaned_data = super(hamyar_form, self).clean()

        return cleaned_data


class login_form(ModelForm):
    user_type = forms.ChoiceField(choices=[(1, 'همیار'), (2, 'مددجو'), (3, 'مددکار'), (4, 'مدیر سامانه')],
                                  label="ورود به عنوانِ")

    class Meta:
        model = models.active_user
        fields = ['username', 'password']

        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'})
        }

    def clean(self):
        cleaned_data = super(login_form, self).clean()
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        type = cleaned_data["user_type"]
        user = authenticate(self.data, username=username, password=password)

        print('!!')
        if user is None:
            # print("!")
            raise forms.ValidationError("kooft")

        return cleaned_data
