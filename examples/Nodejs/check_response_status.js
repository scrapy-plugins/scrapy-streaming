#!/usr/bin/env node

var scrapy = require('scrapystreaming');
var jsonfile = require('jsonfile');

scrapy.createSpider('status', [], function(response) {});

var requests = [200, 201, 400, 404, 500];
var pendingRequests = requests.length;
var result = {};

var canClose = function() {
    if (pendingRequests == 0) {
        jsonfile.writeFile('outputs/check_response.json', result);
        scrapy.closeSpider();
    }
}

var check_response = function(response) {
    result[response.url] = true;
    pendingRequests--;
    canClose();
};

for (req in requests) {
    scrapy.sendRequest('http://httpbin.org/status/' + requests[req], check_response);
}

scrapy.runSpider(function(exception) {
    var msg = JSON.parse(exception.received_message);
    result[msg.url] = false;
    pendingRequests--;
    canClose();
});
