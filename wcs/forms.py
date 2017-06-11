# -*- coding: utf-8 -*-
from django import forms
from .models import Styles
class UploadFileForm(forms.Form):
    file = forms.FileField(label="Завантажте растр у форматі GeoTIFF")
    name_uk = forms.CharField(label="Ім'я файлу українською", required=False)
    note = forms.CharField(label="Опис файлу", required=False)
    epsg = forms.CharField(label="EPSG", required=False)
    style = forms.FileField(label = "Завантажте стиль у форматі .SLD", required=False)
    st = map(lambda i : [i.legend, i.style_name], Styles.objects.all())
    style_select = forms.ChoiceField(st, required=False)
    note.widget.attrs.update({'class': 'form-control', 'type': 'text'})
    epsg.widget.attrs.update({'class': 'form-control', 'type': 'text'})
    name_uk.widget.attrs.update({'class': 'form-control', 'type': 'text'})


class ImportShapefileForm(forms.Form):
    import_file = forms.FileField(label="Оберіть шейп-файл у вигляді .zip-архіву")
    to_db = forms.BooleanField(label="Завантажити до бази даних?", required=False)
    epsg = forms.CharField(label="Epsg", required=False)
    name_uk = forms.CharField(label="Короткий опис файлу", required=False)
    sql_req = forms.CharField(label="SQL - запит (поле=значення)", required=False)
    note = forms.CharField(label="Опис файлу", required=False)
    import_file.widget.attrs.update({'type':'file', 'class':'custom-file-input'})
    to_db.widget.attrs.update({'type':'checkbox', 'class':'form-check-input'})
    epsg.widget.attrs.update({'class':'form-control', 'type':'text'})
    name_uk.widget.attrs.update({'class': 'form-control', 'type': 'text'})
    sql_req.widget.attrs.update({'class': 'form-control', 'type': 'text'})
    note.widget.attrs.update({'class': 'form-control', 'type': 'text'})




