# -*- coding: utf-8 -*-
from geoserver.catalog import Catalog
import zipfile
import tempfile
import os
from osgeo import ogr
from osgeo import osr
import re
import psycopg2
from geoserver.store import *




def import_data(shapefile):

    # Extract the uploaded shapefile.

    fd,fname = tempfile.mkstemp(suffix=".zip")
    os.close(fd)

    f = open(fname, "wb")
    for chunk in shapefile.chunks():
        f.write(chunk)
    f.close()

    if not zipfile.is_zipfile(fname):
        os.remove(fname)
        return "Not a valid zip archive."

    zip = zipfile.ZipFile(fname)

    required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
    has_suffix = {}
    for suffix in required_suffixes:
        has_suffix[suffix] = False

    for info in zip.infolist():
        suffix = os.path.splitext(info.filename)[1].lower()
        if suffix in required_suffixes:
            has_suffix[suffix] = True

    for suffix in required_suffixes:
        if not has_suffix[suffix]:
            zip.close()
            os.remove(fname)
            return "Archive missing required " + suffix + " file."

    shapefile_name = None
    dir_name = tempfile.mkdtemp()
    for info in zip.infolist():
        if info.filename.endswith(".shp"):
            shapefile_name = info.filename

        dst_file = os.path.join(dir_name, info.filename)
        f = open(dst_file, "wb")
        f.write(zip.read(info.filename))
        f.close()
    zip.close()

    # Open the shapefile.
    data = ogr.Open(os.path.join(dir_name, shapefile_name))
    print 0
    layer = data.GetLayer()

    us =  layer.GetSpatialRef()
    us = re.findall('DATUM.+\w', str(us))[0]
    print 2
    conn = psycopg2.connect("dbname='wcs' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    cur.execute("""SELECT srid FROM spatial_ref_sys WHERE srtext ILIKE '%"""+str(us)+"""%' """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    srid = rows[0][0]
    ex = 'GEOMETRYCOLLECTION('
    end = ')'
    for feature in layer:
        geom = feature.GetGeometryRef()
        ex+= geom.ExportToWkt()+','
    ex = ex[:-1]+end

    data = ogr.Open(os.path.join(dir_name, shapefile_name))
    layer = data.GetLayer()
    return ex

def parsing(shapefile):
    # Extract the uploaded shapefile.

    fd, fname = tempfile.mkstemp(suffix=".zip")
    os.close(fd)

    f = open(fname, "wb")
    for chunk in shapefile.chunks():
        f.write(chunk)
    f.close()

    if not zipfile.is_zipfile(fname):
        os.remove(fname)
        return "Not a valid zip archive."

    zip = zipfile.ZipFile(fname)

    required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
    has_suffix = {}
    for suffix in required_suffixes:
        has_suffix[suffix] = False

    for info in zip.infolist():
        suffix = os.path.splitext(info.filename)[1].lower()
        if suffix in required_suffixes:
            has_suffix[suffix] = True

    for suffix in required_suffixes:
        if not has_suffix[suffix]:
            zip.close()
            os.remove(fname)
            return "Archive missing required " + suffix + " file."

    shapefile_name = None
    dir_name = tempfile.mkdtemp()
    for info in zip.infolist():
        if info.filename.endswith(".shp"):
            shapefile_name = info.filename

        dst_file = os.path.join(dir_name, info.filename)
        f = open(dst_file, "wb")
        f.write(zip.read(info.filename))
        f.close()
    zip.close()

    # Open the shapefile.
    data = ogr.Open(os.path.join(dir_name, shapefile_name))
    print 0
    layer = data.GetLayer()
    conn = psycopg2.connect("dbname='wcs' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()
    name_db = layer.GetLayerDefn().GetName()
    try:
        cur.execute("""CREATE TABLE """+name_db+"""(pr_key integer PRIMARY KEY, geom geometry)""")
    except:
        print 'table alredy exist'
    types = {4: 'varchar(256)', 12: 'integer', 2:'float'}
    layer_def = layer.GetLayerDefn()
    field_count = layer_def.GetFieldCount()
    count = 0
    print 'count', layer.GetFeatureCount()
    for feature in layer:
        try:
            cur.execute("""INSERT INTO """ + name_db + """ (pr_key, geom) VALUES (""" + str(count) + """, ST_GeomFromText('"""+str(feature.GetGeometryRef().ExportToWkt())+"""'))""")

        except:
            pass
        count += 1

    for i in range(field_count):
        name = layer_def.GetFieldDefn(i).GetName()
        typer = types[layer_def.GetFieldDefn(i).GetType()]
        width = layer_def.GetFieldDefn(i).GetWidth()
        try:
            cur.execute("""ALTER TABLE """ + name_db + """ ADD COLUMN """+name+""" """+ typer)
        except:
            print 'column alredy exist'
        for k in range(layer.GetFeatureCount()):
            try:
                cur.execute("""UPDATE """+name_db+""" SET """+name+"""= '"""+str(layer.GetFeature(k).GetField(name))+"""' WHERE pr_key = """+ str(k))
            except:
                pass

    conn.commit()
    cur.close()
    conn.close()

    cat = Catalog('http://localhost:8080/geoserver/rest', username='admin', password='geoserver')
    ds = cat.create_datastore(name_db, 'cite')
    ds.connection_parameters.update(host='localhost', port='5432', database='wcs', user='postgres',
                                    passwd='postgres', dbtype='postgis')
    cat.save(ds)
    ft = cat.publish_featuretype(name_db, ds, 'EPSG:4326', srs='EPSG:4326')
    cat.save(ft)


def upload_raster(raster_name, path_to_file):

    try:
        cat = Catalog('http://localhost:8080/geoserver/rest', username='admin', password='geoserver')
        dm = cat.create_coveragestore(raster_name, path_to_file)
        dm.data_url = path_to_file
        cat.save(dm)
    except:
        pass


def upload_style(raster_name,name,path_to_file):
    cat = Catalog('http://localhost:8080/geoserver/rest', username='admin', password='geoserver')
    f = open(path_to_file)
    cat.create_style(name[:-4], f.read())
    style = cat.get_style(name[:-4])
    print 'style name', name
    lyr = cat.get_layer('cite:'+raster_name)
    print 'layer name', 'cite:'+raster_name
    lyr.default_style = style
    cat.save(lyr)

def set_style(style_name, raster_name):
    cat = Catalog('http://localhost:8080/geoserver/rest', username='admin', password='geoserver')
    style = cat.get_style(style_name)
    lyr = cat.get_layer('cite:' + raster_name)
    lyr.default_style = style
    cat.save(lyr)


























