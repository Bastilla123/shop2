
from django import forms

from .models import *
from shop.Widgets import *

module_choices = (
        ('Address', 'Address'),
    )


class Userform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email']
        widgets = {'first_name': textinputfeld, 'last_name': textinputfeld, 'email': textinputfeld,
                   }


    def save(self, commit=True):
            user = super().save(commit=False)

            if commit:
                user.save()
            return user

class Userextendform(forms.ModelForm):
    class Meta:
        model = UserSettings
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user", "boxtabslink",'user_link']

        widgets = { 'street': textinputfeld, 'zip':textinputfeld, 'city':textinputfeld, 'birthdate':datetimepickerfield, 'country':selectfield,'userprofilposition':textinputfeld,
                    'facebook_url': textinputfeld, 'instagram_url': textinputfeld,'company_position': textinputfeld,'description':textarea
                    }

        labels = {'street': "Straße", 'zip': "PLZ", 'city': "Ort",  'birthdate': "Geburtsdatum",  'country':"Land",'basetemplate': "Auswahl Template"
              }


class Settingsform(forms.ModelForm):
    class Meta:
        model = Globalsettings
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user", "boxtabslink"]
        widgets = {
            'client_companyname': textinputfeld, 'client_street': textinputfeld,
            'client_zip': integerfeld, 'client_city': textinputfeld(), 'client_country': selectfield()

        }

    def save(self, commit=True):

        return super().save()
