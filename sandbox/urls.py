import django
from django.apps import apps
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views
from django.urls import include, path
from oscar.views import handler403, handler404, handler500

from apps.sitemaps import base_sitemaps
from globalsettings.urls import urlpatterns as main_urls

admin.autodiscover()
from django.urls import reverse_lazy
urlpatterns = [
    # Include admin as convenience. It's unsupported and only included
    # for developers.
    path('admin/', admin.site.urls),
    #path('globalsettings/', include((main_urls, 'globalsettings'), namespace='globalsettings')),
    path('globalsettings/', include('globalsettings.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('pages/', include('pages.urls')),
    path('clientaddress/', include('clientaddress.urls')),
    path('', include('photo.urls')),

    # i18n URLS need to live outside of i18n_patterns scope of Oscar
    path('i18n/', include(django.conf.urls.i18n)),

    # include a basic sitemap
    path('sitemap.xml', views.index,
        {'sitemaps': base_sitemaps}),
    path('sitemap-<slug:section>.xml', views.sitemap,
        {'sitemaps': base_sitemaps},
        name='django.contrib.sitemaps.views.sitemap')
]

# Prefix Oscar URLs with language codes
urlpatterns += i18n_patterns(
    path('', include(apps.get_app_config('oscar').urls[0])),


)
urlpatterns += i18n_patterns(
    # PayPal Express integration...
    path('checkout/paypal/', include('paypal.express_checkout.urls')),
    # Dashboard views for Payflow Pro
    path('dashboard/paypal/payflow/', apps.get_app_config("payflow_dashboard").urls),
    # Dashboard views for Express
    path('dashboard/paypal/express/', apps.get_app_config("express_dashboard").urls),
    # Dashboard views for Express Checkout
    path('dashboard/paypal/express-checkout/', apps.get_app_config('express_checkout_dashboard').urls),
)

if settings.DEBUG:

    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Allow error pages to be tested
    urlpatterns += [
        path('403', handler403, {'exception': Exception()}),
        path('404', handler404, {'exception': Exception()}),
        path('500', handler500),
        path('__debug__/', include(debug_toolbar.urls)),
    ]
