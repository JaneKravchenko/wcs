# -*- coding: utf-8 -*-
import re
import os
from openpyxl import Workbook
from django.utils.encoding import smart_str
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Attribute, Styles
from pyproj import Proj, transform
from django.core.files import File
from .forms import ImportShapefileForm,  UploadFileForm
from django.http import HttpResponseRedirect
import shapefileio
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from pyproj import Proj, transform
from osgeo import ogr
import psycopg2




def main(request):
    return render_to_response('main.html', {'cs': 'cs'})

def golovna(request):
    return render_to_response('golovna.html', {'cs': 'cs'})
def dopomoga(request):
    return render_to_response('dopomoga.html', {'cs': 'cs'})
def pro_proect(request):
    att = Attribute.objects.all()
    for i in att:
        print i.name_uk
    errMsg = None
    if request.method == "POST":
        print request
        errMsg = None
        form = ImportShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            print 'jane'
            shapefile = request.FILES['import_file']
            epsg = request.POST.get("epsg")
            name_uk = request.POST.get("name_uk")
            sql_req = request.POST.get("sql_req")
            note =  request.POST.get("note")
            to_db = request.POST.get("to_db")
            print 'to_db:', to_db
            print 'EPSG: ', epsg
            print 'name: ', name_uk
            print 'SQL: ', sql_req
            print 'Note: ', note
            errMsg = shapefileio.import_data(shapefile)
            if to_db == 'on':
                wms = "http://localhost:8080/geoserver/cite/wms"
                name_geoserver = 'cite:' + str(file)
                attr = Attribute(translate_name=str(shapefile),
                                 name_uk=name_uk,
                                 sql=sql_req,
                                 wms=wms,
                                 name_geoserver=name_geoserver,
                                 db_name=str(shapefile),
                                 note=note,
                                 req=sql_req)
                attr.save()
                shapefileio.parsing(shapefile)

    form = ImportShapefileForm()
    return render_to_response('pro_proect.html', {'cs': errMsg, 'form': form, 'att':att})
def karta(request):
    return render_to_response('karta.html', {'cs': 'cs'})

def list_shapefiles(request):
    shapefiles = Shapefile.objects.all().order_by('filename')
    return render(request, "list_shapefiles.html" ,{'shapefiles' : shapefiles })

def import_shapefile(request):
    if request.method == "GET":
        form = ImportShapefileForm()
        return render(request, "import_shapefile.html",{'form': form, 'errMsg' : None})
    elif request.method == "POST":
        errMsg = None
        form = ImportShapefileForm(request.POST, request.FILES)
        if form.is_valid():
            shapefile = request.FILES['import_file']

    return render(request, "import_shapefile.html",{'form': form})


def upload_file(request):
    if request.method == 'POST':
        print 'POST METHODS'
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                style = request.FILES['style']
            except:
                style = request.POST.get('style_select')


            epsg = request.POST.get("epsg")
            name_uk = request.POST.get("name_uk")
            note =  request.POST.get("note")
            wms = "http://localhost:8080/geoserver/cite/wms"
            name_geoserver = 'cite:'+str(file)
            attr = Attribute(translate_name=str(file)[:-4],
                      name_uk=name_uk,
                      sql='',
                      wms=wms,
                      name_geoserver=name_geoserver,
                      db_name='',
                      note=note,
                      req='')
            attr.save()
            path_to_folder = 'media/'
            name_of_file = str(file)
            path_to_file = os.path.join(path_to_folder,name_of_file)
            path = default_storage.save(path_to_file, ContentFile(file.read()))
            shapefileio.upload_raster(name_of_file, path_to_file)
            if type(style) != unicode:
                path2 = default_storage.save(os.path.join(path_to_folder,str(style)), ContentFile(style.read()))
                shapefileio.upload_style(name_of_file,str(style),os.path.join(path_to_folder,str(style)))
            else:
                shapefileio.set_style(str(style), name_of_file)
            return HttpResponseRedirect('/pro_proect')
        return render(request, 'import_raster.html', {'form': form})
    else:
        legend = Styles.objects.all()
        form = UploadFileForm()
    return render(request, 'import_raster.html', {'form': form, 'legend':legend})


def inform_point(request):
    print str(request.GET.items()[0][0])
    le = json.loads(str(request.GET.items()[0][0]))
    for feature in le['features']:
        coordinates = feature['geometry']['coordinates']

    x = float(coordinates[0])
    y = float(coordinates[1])
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    coordnew = transform(inProj, outProj, x, y)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(coordnew[0], coordnew[1])

    conn = psycopg2.connect("dbname='wcs' user='postgres' host='localhost' password='postgres'")
    cur = conn.cursor()  


    cur.execute("""SELECT * FROM wcs_nature_reserve_found INNER JOIN wcs_translate_name ON wcs_nature_reserve_found.gid=wcs_translate_name.id  WHERE ST_Intersects(wcs_nature_reserve_found.geom,'"""+str(point)[:-3]+""")'::geometry)""")
    res = cur.fetchall()
    if res:
        colnames = [desc[0] for desc in cur.description]
        wcs = map(lambda i: [colnames[i], res[0][i]], range(len(res[0])))
        name = wcs[3][1]
        print 'wcs', wcs
    else:
        wcs = 1   






    return render(request, 'inform_point.html', {'wcs': wcs, 'name':name})
