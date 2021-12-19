from django.contrib.sitemaps import Sitemap
from .models import *
from django.urls import reverse


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    #def location(self, obj):
    #    return reverse('catalogue', args=[obj.slug,"_",obj.pk])

class StaticSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return ['home', 'about']

