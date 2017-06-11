from __future__ import unicode_literals

from django.contrib.gis.db import models

class Styles(models.Model):
    style_name = models.CharField(max_length = 255, null = False, primary_key=True)
    legend = models.CharField(max_length = 255, null = True)


class Nature_Reserve_Found(models.Model):
    gid = models.IntegerField(primary_key = True, null = False)
    prot_class = models.CharField(max_length=80, null = True)
    prot_stat = models.CharField(max_length=80, null = True)
    prot_title = models.CharField(max_length=99, null = True)
    amenity = models.CharField(max_length=80, null = True)
    leisure = models.CharField(max_length=80, null = True)
    landuse = models.CharField(max_length=80, null = True)
    historic = models.CharField(max_length=80, null = True)
    tourism = models.CharField(max_length=80, null = True)
    website = models.CharField(max_length=110, null = True)
    wikipedia = models.CharField(max_length=103, null = True)
    note = models.CharField(max_length=80, null = True)
    area = models.FloatField(null = True)
    geom = models.MultiPolygonField(null = False)

class Transalte_Name(models.Model):
    id = models.IntegerField(primary_key = True, null = False)
    name = models.CharField(max_length=177, null = True)
    name_uk = models.CharField(max_length=177, null = True)
    name_ru = models.CharField(max_length=177, null = True)
    name_en = models.CharField(max_length=177, null = True)


class Attribute(models.Model):
    translate_name = models.CharField(max_length=255, null = False, primary_key=True)
    name_uk = models.CharField(max_length=255, null = True)
    sql= models.CharField(max_length=255, null=True)
    wms = models.CharField(max_length=255, null=True)
    name_geoserver = models.CharField(max_length=255, null=True)
    db_name = models.CharField(max_length=255, null=True)
    note = models.CharField(max_length=255, null=True)
    req = models.CharField(max_length=255, null=True)
    style=models.CharField(max_length=255, null=True)







