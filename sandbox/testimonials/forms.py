from bibliothek.Widgets import *
from bibliothek.FormMixins import *
from .models import Testimonialmodel
#from multi_form_view import MultiFormView,MultiModelFormView,MultiModelForm

#class Testimonialform2(MultiModelForm):
#    form_classes = {
#        'user': UserCreationForm,#
    #    'profile': UserProfileForm,
    #}

class Testimonialform(StandardMixin):
    class Meta:
        model = Testimonialmodel
        exclude = ["id", "trash", "is_deleteable", "is_editable", "create_date", "is_active", "modified_date",
                   "create_user", "modified_user", "delete_user","boxtabslink","image"]


        labels = {'name': "Name",
              }