#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var fs = require('fs');


scrapy.createSpider('utf8sample', [], function(response) {});
scrapy.sendRequest('http://httpbin.org/encoding/utf8', function(response) {
    fs.writeFile('outputs/utf8.html', response.body);
    scrapy.closeSpider();
});

scrapy.runSpider();
