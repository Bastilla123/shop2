import oscar.apps.dashboard.apps as apps
from django.urls import path
from django.conf.urls import url
from .views import *



from oscar.core.loading import get_class


class DashboardConfig(apps.DashboardConfig):

    name = 'dashboard'
    def ready(self):
        super().ready()
        self.flash_sale_create_view = get_class('dashboard.offers.views', 'FlashSaleCreateView')

    def get_urls(self):

        urls = [
            path('new/flash-sale/<int:product_pk>/', self.flash_sale_create_view.as_view(),
                name='create-flash-sale'),
            #url(r'^transactions/$', self.TransactionListView.as_view(),
            #    name='cashondelivery-transaction-list'),
            #url(r'^transactions/(?P<pk>\d+)/$', self.TransactionDetailView.as_view(),
            #    name='cashondelivery-transaction-detail'),
        ]

        return super().get_urls() + self.post_process_urls(urls)




