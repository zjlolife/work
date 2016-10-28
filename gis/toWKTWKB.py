import os, GisConvert
from shapely import geos

geos.WKBWriter.defaults['include_srid'] = True
fileNames = os.listdir('amapToBaidu')
wkbFile = open('district_boundary.csv', 'w')
wkbDatas = '';
id = 1;
for fileName in fileNames :
    file = open('amapToBaidu/' + fileName, 'r')
    data = file.read()
    polylines = data.split('|')
    polygon = GisConvert.toPolygon(polylines)
    geos.lgeos.GEOSSetSRID(polygon._geom, 900913)
    if polygon.is_valid :
        wFile = open('amapWKT/' + fileName, 'w')
        wFile.write(polygon.wkt)
        wkbData = polygon.wkb.encode('hex')
        district = fileName.split('_');
        districtCode = district[0]
        districtName = district[1]
        cityId = district[2]
        cityId = cityId[0:cityId.index('.')]
        wkbDatas += str(id) + ',' + cityId + ',' + districtCode + ',' + districtName + ',' + wkbData + '\n'
        id += 1
    else :
        print fileName + "-inValid"
wkbFile.write(wkbDatas)
