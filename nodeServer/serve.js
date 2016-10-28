var express = require('express');
var http = require('http');
var app = express();
var fs = require("fs");
var request = require('sync-request');

app.get('/getAmapBoundary', function(req, res){
   var district = req.query.district;
    var ampUrl = "/service/poiInfo?query_type=TQUERY&keywords=" + district;
    var options = {
      hostname: 'ditu.amap.com',
      port: 80,
      method: 'GET',
      path: encodeURI(ampUrl)
    };
    var data = "";
    var req1 = http.request(options, function(res1){
      res1.on('data', function(chunk) {
        data += chunk;
      })
      res1.on('end' ,function () {
         res.setHeader("Content-Type", "application/json;charset=UTF-8");
         console.log(data)
         res.end(data);
      })
    });
    req1.end();
})

app.get('/getAmapBoundary1', function (req, res) {
    var district = req.query.district;
    var files = fs.readdirSync('ampBoundary');
    console.log(files);
    for (i=0;i<files.length;i++) {
        file = files[i];
        if (file.indexOf(district)) {
            var data = fs.readFileSync('ampBoundary/' + file);
            console.log(data);
            res.setHeader("Content-Type", "application/json;charset=UTF-8");
            var result = {data : data.toString()};
            res.end(JSON.stringify(result));
            return;
        }
    }
})


app.get('/amapToBaiduBoundary', function (req, res) {
    var district = req.query.district;
    var files = fs.readdirSync('ampToBaiduBoundary');
    for (i=0;i<files.length;i++) {
        file = files[i];
        if (file.indexOf(district) > -1) {
            console.log(file);
            var data = fs.readFileSync('ampToBaiduBoundary/' + file);
            res.setHeader("Content-Type", "application/json;charset=UTF-8");
            var result = {data : data.toString()};
            res.end(JSON.stringify(result));
            return;
        }
    }
})

app.get('/amap.html', function (req, res) {
  var data = fs.readFileSync('amap.html', 'utf-8');
  res.setHeader("Content-Type", "text/html");
  res.end(data);
})

app.get('/amap1.html', function (req, res) {
  var data = fs.readFileSync('amap1.html', 'utf-8');
  res.setHeader("Content-Type", "text/html");
  res.end(data);
})

app.get('/baiduMap.html', function (req, res) {
  var data = fs.readFileSync('baiduMap.html', 'utf-8');
  res.setHeader("Content-Type", "text/html");
  res.end(data);
})

var server = app.listen(8081, function () {

  var host = server.address().address
  var port = server.address().port

  console.log("应用实例，访问地址为 http://%s:%s", host, port)

})
