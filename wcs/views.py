# -*- coding: utf-8 -*-
import re
import os
from openpyxl import Workbook
from django.utils.encoding import smart_str
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Shapefile
from pyproj import Proj, transform
from django.core.files import File
from .forms import ImportShapefileForm
from django.http import HttpResponseRedirect
import shapefileio
def main(request):
    return render_to_response('main.html', {'cs': 'cs'})

def golovna(request):
    return render_to_response('golovna.html', {'cs': 'cs'})
def dopomoga(request):
    return render_to_response('dopomoga.html', {'cs': 'cs'})
def pro_proect(request):
    return render_to_response('pro_proect.html', {'cs': 'cs'})
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
            errMsg = shapefileio.import_data(shapefile)
            if errMsg == None:
                return HttpResponseRedirect("/")
    return render(request, "import_shapefile.html",{'form': form, 'errMsg' : errMsg })