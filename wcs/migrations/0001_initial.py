# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-08 19:26
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.IntegerField()),
                ('width', models.IntegerField()),
                ('precision', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wcs.Attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom_point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('geom_multipoint', django.contrib.gis.db.models.fields.MultiPointField(blank=True, null=True, srid=4326)),
                ('geom_multilinestring', django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326)),
                ('geom_multipolygon', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('geom_geometrycollection', django.contrib.gis.db.models.fields.GeometryCollectionField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Shapefile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('srs_wkt', models.CharField(max_length=255)),
                ('geom_type', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='feature',
            name='shapefile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wcs.Shapefile'),
        ),
        migrations.AddField(
            model_name='attributevalue',
            name='feature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wcs.Feature'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='shapefile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wcs.Shapefile'),
        ),
    ]
