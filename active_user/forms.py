from django.forms import ModelForm, forms
from django import forms
from active_user import models
from active_user.models import hamyar
from django.utils.translation import ugettext_lazy as _



class hamyar_form(ModelForm):
    class Meta:
        model = models.hamyar
        fields = ['username', 'password', 'first_name', 'last_name', 'id_number', 'phone_number', 'email', 'address']

        # error_messages = {
        #     'username': {
        #         'afra': _("این نام کاربری قبلا انتخاب شده است."),
        #     },
        #     'id_number': {
        #         'afra': _("کد ملی در سیستم ثبت شده است."),
        #     },
        # }

    def clean(self):
        cleaned_data = super(hamyar_form, self).clean()
        usernames = hamyar.objects.filter(username=cleaned_data.get("username")).count()
        print(usernames)
        if usernames > 0:
            forms.ValidationError('salam')
            # self.add_error('username', 'This username has been taken')

        # id_numbers = hamyar.objects.filter(id_number=cleaned_data.get("id_number")).count()
        # if id_numbers > 0:
        #     forms.ValidationError(self.fields['id_number'].error_messages['afra'])

        return cleaned_data

class login_form(ModelForm):

    user_type = forms.ChoiceField(choices=[(1, 'مدیر سامانه'), (2, 'مددجو'), (3, 'مددکار'), (4, 'همیار')], label="ورود به عنوانِ")
    class Meta:
        model = models.active_user
        fields = ['username', 'password']
