#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var jsonfile = require('jsonfile');
var cheerio = require('cheerio');

var pendingRequests = 0;
var result = {};

var parse = function(response) {
    var $ = cheerio.load(response.body);

    $('#subcategories-div > section > div > div.cat-item > a').each(function(i, item) {
        scrapy.sendRequest('http://www.dmoz.org' + $(this).attr('href'), parse_cat);
        pendingRequests++;
    });
};

var parse_cat = function(response) {
    var $ = cheerio.load(response.body);

    $('div.title-and-desc a').each(function(i, item) {
        result[$(this).text().trim()] = $(this).attr('href');
    });

    pendingRequests--;
    if (pendingRequests == 0) {
        jsonfile.writeFile('outputs/dmoz_data.json', result);
        scrapy.closeSpider();
    }
};

var check_response = function(response) {
    result[response.url] = true;
    pendingRequests--;
    canClose();
};

scrapy.createSpider('dmoz', ["http://www.dmoz.org/Computers/Programming/Languages/Python/"], parse);
scrapy.runSpider();
