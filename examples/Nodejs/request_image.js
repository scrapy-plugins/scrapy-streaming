#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var fs = require('fs');


scrapy.createSpider('image', [], function(response) {});
scrapy.sendRequest('http://httpbin.org/image/png', function(response) {
    fs.writeFile('outputs/image.png', response.body, {encoding: 'base64'});
    scrapy.closeSpider();
},  {base64: true});

scrapy.runSpider();
