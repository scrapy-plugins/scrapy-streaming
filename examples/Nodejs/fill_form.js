#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var jsonfile = require('jsonfile');

scrapy.createSpider('form', [], function(response) {});

var fromResponseRequest = {
    formdata: {
        custname: 'Sample',
        custemail: 'email@example.com'
    }
};

scrapy.sendFromResponseRequest('http://httpbin.org/forms/post', function(response) {
    jsonfile.writeFile('outputs/fill_form.json', response.body);
    scrapy.closeSpider();
}, fromResponseRequest);

scrapy.runSpider();
