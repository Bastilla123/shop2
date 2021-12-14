from globalsettings.models import Globalsettings
from oscar.apps.basket.views import BasketView as CoreBasketView

class BasketView(CoreBasketView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['globalsettings'] =  Globalsettings.objects.first()
        print("Context "+str(context))
        return context