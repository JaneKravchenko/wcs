# -*- coding: utf-8 -*-

import zipfile
import tempfile
import os

def import_data(shapefile):
    fd, fname = tempfile.mkstemp(suffix=".zip")
    os.close(fd)
    f = open(fname, "wb")
    for chunk in shapefile.chunks():
        f.write(chunk)
    f.close()
    if not zipfile.is_zipfile(fname):
        os.remove(fname)
        return "Недопустимый архив ZIP ."
    zip1 = zipfile.ZipFile(fname)
    required_suffixes = [".shp", ".shx", ".dbf", ".prj"]
    has_suffix = {}
    for suffix in required_suffixes:
        has_suffix[suffix] = False
    for info in zip1.infolist():
        suffix = os.path.splitext(info.filename)[1].lower()
        if suffix in required_suffixes:
            has_suffix[suffix] = True
    for suffix in required_suffixes:
        if not has_suffix[suffix]:
            zip1.close()
            os.remove(fname)
            return "В архиве отсутствует необходимый " + suffix + " файл."
        else:
            return "Всё хорошо."