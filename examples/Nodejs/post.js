#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var jsonfile = require('jsonfile');

scrapy.createSpider('post', [], function(response) {});

scrapy.sendRequest('http://httpbin.org/post', function(response) {
    jsonfile.writeFile('outputs/post.json', response.body);
    scrapy.closeSpider();
}, {method: 'POST', body: 'Post data'});

scrapy.runSpider();
