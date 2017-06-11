from osgeo import gdal
import sys
import numpy as np


def main(band_num, input_file):
    src_ds = gdal.Open( input_file )
    if src_ds is None:
        print 'Unable to open %s' % input_file
        sys.exit(1)

    try:
        srcband = src_ds.GetRasterBand(band_num).ReadAsArray().astype(np.float)
    except RuntimeError, e:
        print 'No band %i found' % band_num
        print e
        sys.exit(1)


    #print "[ MIN ] = ", srcband.GetMinimum()
    #print "[ MAX ] = ", srcband.GetMaximum()
    #print "[ SCALE ] = ", srcband.GetScale()
    #print "[ UNIT TYPE ] = ", srcband.GetUnitType()
    return srcband

def ndvi(band4, band5, clip_shape = None):
    if clip_shape == None:
        return (band5-band4)/(band5+band4)

def saveRaster(outPath, etalonPath, array):
    gdalData = gdal.Open(etalonPath)
    projection = gdalData.GetProjection()
    transform = gdalData.GetGeoTransform()
    xsize = gdalData.RasterXSize
    ysize = gdalData.RasterYSize
    gdalData = None

    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    metadata = driver.GetMetadata()
    if metadata.has_key(gdal.DCAP_CREATE) and metadata[gdal.DCAP_CREATE] == "YES":
        outRaster = driver.Create(outPath, xsize, ysize, 1, gdal.GDT_Byte)
        outRaster.SetProjection(projection)
        outRaster.SetGeoTransform(transform)
        outRaster.GetRasterBand(1).WriteArray(array)
        outRaster = None
    else:
        print "Driver %s does not support Create() method." % format
        return False

path4 = '/home/jane/Desktop/university/Diploma/Data/LC08_L1TP_180026_20170506_20170515_01_T1/LC08_L1TP_180026_20170506_20170515_01_T1_B4.TIF'
path5 = '/home/jane/Desktop/university/Diploma/Data/LC08_L1TP_180026_20170506_20170515_01_T1/LC08_L1TP_180026_20170506_20170515_01_T1_B5.TIF'

srcband4 = main(1, path4)
srcband5 = main(1,path5)
nd = ndvi(srcband4, srcband5)
saveRaster('/home/jane/Desktop/out.tif', path4, nd)


