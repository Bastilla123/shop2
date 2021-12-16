from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProduct


class Tax(models.Model):
    Taxlabel = models.TextField(default="",blank=False,null=False)
    Taxvalue = models.PositiveSmallIntegerField( blank=True, default=0, null=True)

    def __str__(self):
        return self.Taxlabel


class colorchoices(models.Model):
    name = models.CharField(default="",max_length=80, blank=False, null=False)

    def __str__(self):
        return self.name

class sizechoices(models.Model):
    name = models.CharField(default="",max_length=80, blank=False, null=False)
    def __str__(self):
        return self.name

class brandchoices(models.Model):
    name = models.CharField(default="",max_length=80, blank=False, null=False)
    def __str__(self):
        return self.name

class materialchoices(models.Model):
    name = models.CharField(default="",max_length=80, blank=False, null=False)
    def __str__(self):
        return self.name

class Product(AbstractProduct):
    product_tax = models.ForeignKey(Tax, on_delete=models.CASCADE, blank=True, null=True, default=None,
                              related_name="product_tax")
    size = models.ForeignKey(sizechoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                   related_name="size_choices")
    color = models.ForeignKey(colorchoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                             related_name="colour_choices")
    brand = models.ForeignKey(brandchoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                               related_name="brand_choices")
    material = models.ForeignKey(materialchoices, on_delete=models.CASCADE, blank=True, null=True, default=None,
                              related_name="material_choices")

from oscar.apps.catalogue.models import *
