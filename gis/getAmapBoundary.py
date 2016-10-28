# coding=utf-8
import requests, time, json, os


if not os.path.exists('amapBoundary') :
    os.mkdir('amapBoundary')

file = open('district_prod.lst', 'r')
while 1 :
    line = file.readline();
    if not line :
        break
    arr = line.split(',')
    districtCode = arr[0]
    districtName = arr[1]
    cityId = arr[2]
    keywords = arr[3]
    outFileName = 'amapBoundary/' + districtCode + '_' +districtName + '_' + cityId + '.lst'
    if os.path.exists(outFileName) :
        continue
    ampUrl = "http://restapi.amap.com/v3/config/district?keywords="+ districtCode + "&extensions=all&key=fd37881b4dd5246eb371571968d7a345";
    resStr = requests.get(ampUrl);
    res = json.loads(resStr.text);
    districts = res['districts'];
    if (len(districts) == 0) :
        ampUrl1 = "http://restapi.amap.com/v3/config/district?keywords="+ districtName + "&extensions=all&key=fd37881b4dd5246eb371571968d7a345";
        resStr1 = requests.get(ampUrl1);
        res1 = json.loads(resStr1.text);
        districts1 = res1['districts'];
        if (len(districts1) == 1) :
            polyline = districts1[0]['polyline'];
            outFile = open(outFileName, 'w');
            outFile.write(polyline);
        else :
            print res
            print districtCode + districtName + "boundary not get"
    elif (len(districts) == 1) :
        polyline = districts[0]['polyline'];
        outFile = open(outFileName, 'w');
        outFile.write(polyline);
    else :
        print res
        print districtCode + districtName + "boundary not get"
