# coding=utf-8
import requests, time, json, os, GisConvert

url = 'http://ditu.amap.com/service/poiInfo?query_type=TQUERY&keywords='

if not os.path.exists('amapProdBoundary') :
    os.mkdir('amapProdBoundary')

file = open('amap_errorBoundary.lst', 'r')
while 1 :
    line = file.readline();
    if not line :
        break
    arr = line.split(',')
    districtCode = arr[0]
    districtName = arr[1]
    cityId = arr[2]
    keywords = arr[3]
    outFileName = 'amapProdBoundary/' + districtCode + '_' +districtName + '_' + cityId + '.lst'
    if os.path.exists(outFileName) :
        continue
    time.sleep(10)
    resStr = requests.get('http://ditu.amap.com/service/poiInfo?query_type=TQUERY&keywords=' + keywords)
    res = json.loads(resStr.text)
    if res['status'] == '1' :
        data = res['data'][0]['list'][0]['coords']
        polylines = data.split('@')
        dPolylines = [];
        for polyline in polylines :
            lngLats = polyline.split(';')
            length = len(lngLats)
            count = length / 2
            dLngLats = [];
            for index in range(count) :
                dLngLats.append(lngLats[2 * index] + ',' + lngLats[2 * index + 1])

            dPolylines.append(';'.join(dLngLats))
        polygon = GisConvert.toPolygon(dPolylines)
        if polygon.is_valid :
            print districtName
            outFile = open(outFileName, 'w')
            outFile.write('|'.join(dPolylines))
            wktFile = open('amapProdBoundary/' + districtName + '.wkt', 'w')
            wktFile.write(polygon.wkt)
        else :
            print districtCode + districtName + "高德数据反爬虫返回错误数据或该边界数据存在交叉"
    else :
        print res
        print districtCode + districtName + "boundary not get"
