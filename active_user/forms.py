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
        # usernames = hamyar.objects.filter(username=cleaned_data.get("username")).count()
        # print(usernames)
        # if usernames > 0:
        #     forms.ValidationError(self.fields['username'].error_messages['unique'])

        # id_numbers = hamyar.objects.filter(id_number=cleaned_data.get("id_number")).count()
        # if id_numbers > 0:
        #     forms.ValidationError(self.fields['id_number'].error_messages['afra'])

        return cleaned_data


class login_form(ModelForm):

    user_type = forms.ChoiceField(choices=[(1, 'مدیر سامانه'), (2, 'مددجو'), (3, 'مددکار'), (4, 'همیار')], label="ورود به عنوانِ")
    class Meta:
        model = models.active_user
        fields = ['username', 'password']


    def clean(self):
        cleaned_data = super(login_form, self).clean()
        username = cleaned_data["username"]
        password = cleaned_data["password"]
        type = cleaned_data["user_type"]
        user = authenticate(self.data, username=username, password=password)

        table_type = [models.madadjoo, models.madadkar, models.hamyar]
        user_panel = ["admin_panel", "madadjoo_panel", "madadkar_panel", "hamyar_panel"]

        print('!!')
        if user is None:
            # print("!")
            raise forms.ValidationError("kooft")

        return cleaned_data

