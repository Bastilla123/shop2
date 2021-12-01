from django.db import models
from django.contrib.auth.models import User


class Standard_Model_Mixin(models.Model):
    is_deleteable = models.BooleanField(default=True)
    is_editable = models.BooleanField(default=True)
    create_date = models.DateTimeField(default=None,null=True)
    is_active = models.BooleanField(default=True)
    modified_date = models.DateTimeField(default=None,null=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                    related_name="%(class)s_create_user", )
    modified_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                      related_name="%(class)s_modified_user", )
    delete_user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                    related_name="%(class)s_delete_user", )


    trash = models.BooleanField(default=False)
    class Meta:
        abstract = True




def get_repr(value):

        if callable(value) and 'None' not in str(value) and str(value) != 'auth.User.None' and 'Rights' not in str(value) and str(value) != 'address.Telefax.None' and str(value) != 'address.Telefon.None' and str(value) != 'address.Email.None'   :

            return '%s' % value()
        return value

def get_field(instance, field):
        field_path = field.split('.')
        attr = instance

        for elem in field_path:

            if ('rights' in elem):
                continue
            try:
                attr = getattr(attr, elem)
            except AttributeError:
                return None
        return attr


class LoggerModelMixin():

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in [field.name for field in self._meta.get_fields()]:


            if (not hasattr(self,'id') or self.id is None):

                setattr(self, '__original_%s' % fieldname, None)
            else:
                setattr(self, '__original_%s' % fieldname, get_repr(get_field(self, fieldname)))

    def has_changed(self,request):

        String = ""
        changed = False
        for field in [f.name for f in self._meta.fields]:

            orig = '__original_%s' % field
            if getattr(self, orig) != getattr(self, field):
                if (changed == False):
                    changed = True

                String += "(Feldbezeichnung: " + str(field) + " --"

                if ('edit' in request.get_full_path()):
                    if (str(getattr(self, orig)).strip() != ""):

                        String += " Alter Wert: " + str(
                        getattr(self, orig))+ " --"

                String +=    " Neuer Wert: " + str(getattr(self, field)) + ")\n"

        return changed, String
