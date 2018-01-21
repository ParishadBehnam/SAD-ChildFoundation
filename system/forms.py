from django.forms import ModelForm
from active_user import models


class madadjoo_information_form(ModelForm):
    class Meta:
        model = models.madadjoo
        fields = ['first_name', 'last_name', 'id_number', 'phone_number', 'email', 'invest_percentage',
                  'address', 'successes', 'bio', 'edu_status'] #TODO نیاز :-اس

    def clean(self):
        cleaned_data = super(madadjoo_information_form, self).clean()

        return cleaned_data