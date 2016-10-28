# coding=utf-8
import os, GeoConverter

fileNames = os.listdir('amapBoundary')


if not os.path.exists('amapToBaidu') :
    os.mkdir('amapToBaidu')

for fileName in fileNames :
    print fileName
    file = open('amapBoundary/' + fileName, 'r')
    data = file.read()
    polylines = data.split('|')
    dPolylines = [];
    for polyline in polylines :
        lngLats = polyline.split(';')
        length = len(lngLats)
        dLngLats = [];
        for lngLat in lngLats :
            lngLatArr = lngLat.split(',')
            dLngLatArr = GeoConverter.gcj2bd([float(lngLatArr[1]), float(lngLatArr[0])])
            dLngLats.append(str(dLngLatArr[1]) + ',' + str(dLngLatArr[0]))

        dPolylines.append(';'.join(dLngLats))

    outFile = open('amapToBaidu/' + fileName, 'w')
    outFile.write('|'.join(dPolylines))
