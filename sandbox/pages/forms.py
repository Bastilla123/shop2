from django import forms
from clientaddress.models import *
from bibliothek.Widgets import *


class Widerrufform(forms.ModelForm):

    class Meta:

        model = Clientaddress
        exclude = ["id","trash","is_deleteable","is_editable","create_date","modified_date","create_user","modified_user","delete_user",'user_rights_link','addressindividualfields','searchvriteria_address_link','Telefon_address_link','Email_address_link','Telefax_address_link','group_rights-link','change_date','owner','occurrence','searchcriteria_address_link','task_assigned_to']
        widgets = {'salutation': selectfield, 'firstname': textinputfeld, 'lastname': textinputfeld, 'companyname': textinputfeld, 'street': textinputfeld, 'zip': integerfeld, 'city': textinputfeld}
    def __init__(self, *args, **kwargs):


        super().__init__(*args, **kwargs)

        self.fields['product'] =  forms.CharField(
            widget=textinputfeld,
            required=False)
        self.fields['order_date'] = forms.CharField(
            widget=textinputfeld,
            required=False)
        self.fields['email'] = forms.EmailField(max_length = 200,widget=textinputfeld,
            required=True)

