var assert = require('chai').assert;


describe('Initialization', function() {
    spider = require('../index.js');
    it('start with null / empty values', function(){
        assert.equal(spider.exceptionHandler, null);
    });
});


describe('runSpider', function() {
    spider = require('../index.js');

    it('raises exception with wrong exceptionHandler', function() {
        assert.throws(function(){spider.runSpider(1)}, Error);
        assert.throws(function(){spider.runSpider('test')}, Error);
        assert.throws(function(){spider.runSpider(null)}, Error);
    });

    it('updates exceptionHandler', function() {
        var testFunction = function(){};
        spider.runSpider(testFunction);
        assert.equal(spider.exceptionHandler, testFunction);
    });
});


describe('closeSpider', function() {
    spider = require('../index.js');
    msg = spider.closeSpider();
    var expected_msg = {
        type: 'close'
    };

    it('correct close message', function() {
        assert.deepEqual(JSON.parse(msg), expected_msg);
    });
});


describe('createSpider', function() {
    spider = require('../index.js');

    it('check required fields', function() {
        assert.throws(function(){spider.createSpider()}, 'Error: missing name');
        assert.throws(function(){spider.createSpider('name')}, 'Error: missing startUrls');
        assert.throws(function(){spider.createSpider('name', [])}, 'Error: missing callback');
    });

    it('validate field type', function() {
        //name
        assert.throws(function(){spider.createSpider(1, [], function(){})}, 'name parameter must be string');
        assert.doesNotThrow(function(){spider.createSpider('name', [], function(){})});

        //startUrls
        assert.throws(function(){spider.createSpider('name', 1, function(){})}, 'startUrls parameter must be an array');
        assert.doesNotThrow(function(){spider.createSpider('name', [], function(){})});

        //callback
        assert.throws(function(){spider.createSpider('name', [], 11)}, 'callback parameter must be function');
        assert.doesNotThrow(function(){spider.createSpider('name', [], function(){})});

        //allowedDomains
        assert.throws(function(){spider.createSpider('name', [], function(){}, 1)}, 'allowedDomains parameter must be an array');
        assert.doesNotThrow(function(){spider.createSpider('name', [], function(){}), []});

        //customSettings
        assert.throws(function(){spider.createSpider('name', [], function(){}, null, 3)}, 'customSettings parameter must be object');
        assert.doesNotThrow(function(){spider.createSpider('name', [], function(){}), null, {test: 1}});
    });

    it('generate the json message', function() {
        var expected_msg = {
            type: 'spider',
            name: 'name',
            start_urls: ['http://example.com'],
            allowed_domains: ['example.com'],
            custom_settings: {test: 1}
        };

        var msg = spider.createSpider(expected_msg.name, expected_msg.start_urls, function(){},
                                      expected_msg.allowed_domains, expected_msg.custom_settings);

        assert.deepEqual(JSON.parse(msg), expected_msg);
    });
});


describe('sendLog', function() {
    spider = require('../index.js');

    it('check required fields', function() {
        assert.throws(function(){spider.sendLog()}, 'Error: missing message');
        assert.throws(function(){spider.sendLog('name')}, 'Error: missing level');
    });

    it('validate field type', function() {
        //message
        assert.throws(function(){spider.sendLog(1, 'debug')}, 'message parameter must be string');
        assert.doesNotThrow(function(){spider.sendLog('name', 'debug')});

        //level
        assert.throws(function(){spider.sendLog('name', 1)}, 'level parameter must be string');
        assert.doesNotThrow(function(){spider.sendLog('name', 'debug')});
    });

    it('check debug level', function() {
        assert.doesNotThrow(function(){spider.sendLog('name', 'critical')});
        assert.doesNotThrow(function(){spider.sendLog('name', 'error')});
        assert.doesNotThrow(function(){spider.sendLog('name', 'warning')});
        assert.doesNotThrow(function(){spider.sendLog('name', 'info')});
        assert.doesNotThrow(function(){spider.sendLog('name', 'debug')});
        assert.throws(function(){spider.sendLog('name', 'aaa')}, 'Invalid log level. Must be one of ');
    });

    it('generate the json message', function() {
        var expected_msg = {
            type: 'log',
            message: 'message',
            level: 'DEBUG'
        };

        var msg = spider.sendLog(expected_msg.message, expected_msg.level);

        assert.deepEqual(JSON.parse(msg), expected_msg);
    });
});


describe('sendRequest', function() {
    spider = require('../index.js');

    //    url, callback, base64, method, meta, body, headers, cookies, encoding, priority, dontFilter
    it('check required fields', function() {
        assert.throws(function(){spider.sendRequest()}, 'Error: missing url');
        assert.throws(function(){spider.sendRequest('http://example.com')}, 'Error: missing callback');
    });

    it('validate field type', function() {
        //url
        assert.throws(function(){spider.sendRequest(1, function(){})}, 'url parameter must be string');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){})});

        //callback
        assert.throws(function(){spider.sendRequest('http://example.com', 1)}, 'callback parameter must be function');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){})});

        //base64
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {base64: 1})},
                                                    'base64 parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {base64: false})});

        //method
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {method: 1})},
                                                    'method parameter must be string');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {method: 'get'})});

        //meta
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {meta: 1})},
                                                                'meta parameter must be object');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {meta: {}})});

        //body
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {body: 1})},
                                                                'body parameter must be string');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {body: 'body'})});

        //headers
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {headers: 'Content-type'})},
                                                                'headers parameter must be object');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {headers: {}})});

        //cookies
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {cookies: 'a'})},
                                                  'cookies parameter must be object');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {cookies: {}})});

        //encoding
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {encoding: 1})},
                                                  'encoding parameter must be string');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {encoding: 'utf8'})});

        //priority
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {priority: 'high'})},
                                                  'priority parameter must be number');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {priority: 1})});

        //dont_filter
        assert.throws(function(){spider.sendRequest('http://example.com', function(){}, {dont_filter: 1})},
                                                  'dont_filter parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendRequest('http://example.com', function(){}, {dont_filter: true})});
    });

    it('generate the json message', function() {

        var config = {
            base64: true,
            method: 'get',
            meta: {a: 1},
            body: 'body',
            headers: {b: 2},
            cookies: {c: 3},
            encoding: 'utf8',
            priority: 1,
            dont_filter: true
        };

        var expected_msg = {
            type: 'request',
            url: 'http://example.com',
            id: spider._requestId,
            base64: config.base64,
            method: config.method,
            meta: config.meta,
            body: config.body,
            headers: config.headers,
            cookies: config.cookies,
            encoding: config.encoding,
            priority: config.priority,
            dont_filter: config.dont_filter
        };


        var msg = spider.sendRequest(expected_msg.url, function(){}, config);

        assert.deepEqual(JSON.parse(msg), expected_msg);
    });

    it('register the callback', function(){
        var responseId = spider._requestId;
        var callback = function() {};

        var msg = spider.sendRequest('http://example.com', callback);
        assert.equal(spider.responseMapping[responseId], callback);
    })
});


describe('sendFromResponseRequest', function() {
    spider = require('../index.js');

    //    url, callback, base64, method, meta, body, headers, cookies, encoding, priority, dontFilter
    it('check required fields', function() {
        assert.throws(function(){spider.sendFromResponseRequest()}, 'Error: missing url');
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com')}, 'Error: missing callback');
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){})}, 'Error: missing fromResponseRequest');
    });

    it('validate field type', function() {
        //url
        assert.throws(function(){spider.sendFromResponseRequest(1, function(){}, {})}, 'url parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {})});

        //callback
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', 1, {})}, 'callback parameter must be function');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {})});

        //fromResponseRequest
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, 1)}, 'fromResponseRequest parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {})});

        //base64
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {base64: 1})},
                                                    'base64 parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {base64: false})});

        //method
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {method: 1})},
                                                    'method parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {method: 'get'})});

        //meta
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {meta: 1})},
                                                                'meta parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {meta: {}})});

        //body
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {body: 1})},
                                                                'body parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {body: 'body'})});

        //headers
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {headers: 'Content-type'})},
                                                                'headers parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {headers: {}})});

        //cookies
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {cookies: 'a'})},
                                                  'cookies parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {cookies: {}})});

        //encoding
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {encoding: 1})},
                                                  'encoding parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {encoding: 'utf8'})});

        //priority
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {priority: 'high'})},
                                                  'priority parameter must be number');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {priority: 1})});

        //dont_filter
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {dont_filter: 1})},
                                                  'dont_filter parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {}, {dont_filter: true})});
    });

    it('validate fromResponseRequest fields type', function() {
        //url
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {url: 1})}, 'url parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {url: 'http://example.com'})});

        //method
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {method: 1})},
                                                    'method parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {method: 'get'})});

        //meta
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {meta: 1})},
                                                                'meta parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {meta: {}})});

        //body
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {body: 1})},
                                                                'body parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {body: 'body'})});
//url
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {method: 'get'})});

        //meta
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {meta: 1})},
                                                                'meta parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {meta: {}})});

        //body
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {body: 1})},
                                                                'body parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {body: 'body'})});

        //headers
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {headers: 'Content-type'})},
                                                                'headers parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {headers: {}})});

        //cookies
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {cookies: 'a'})},
                                                  'cookies parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {cookies: {}})});

        //encoding
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {encoding: 1})},
                                                  'encoding parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {encoding: 'utf8'})});

        //priority
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {priority: 'high'})},
                                                  'priority parameter must be number');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {priority: 1})});

        //dontFilter
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {dont_filter: 1})},
                                                  'dont_filter parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {dont_filter: true})});
        //headers
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {headers: 'Content-type'})},
                                                                'headers parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {headers: {}})});

        //cookies
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {cookies: 'a'})},
                                                  'cookies parameter must be object');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {cookies: {}})});

        //encoding
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {encoding: 1})},
                                                  'encoding parameter must be string');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {encoding: 'utf8'})});

        //priority
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {priority: 'high'})},
                                                  'priority parameter must be number');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {priority: 1})});

        //dontFilter
        assert.throws(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {dont_filter: 1})},
                                                  'dont_filter parameter must be boolean');
        assert.doesNotThrow(function(){spider.sendFromResponseRequest('http://example.com', function(){}, {dont_filter: true})});
    });


    it('generate the json message', function() {
        var config = {
            base64: true,
            method: 'get',
            meta: {a: 1},
            body: 'body',
            headers: {b: 2},
            cookies: {c: 3},
            encoding: 'utf8',
            priority: 1,
            dont_filter: true
        };

        var expected_msg = {
            type: 'from_response_request',
            url: 'http://example.com',
            id: spider._requestId,
            from_response_request: {
                url: 'http://example.com/login',
                method: 'get',
                meta: {a: 1},
                body: 'body',
                headers: {b: 2},
                cookies: {c: 3},
                encoding: 'utf8',
                priority: 1,
                dont_filter: true,
                formname: 'name',
                formxpath: 'xpath',
                formcss: 'css',
                formnumber: 1,
                formdata: {a: 1},
                clickdata: {b: 2},
                dont_click: true,
            },
            base64: config.base64,
            method: config.method,
            meta: config.meta,
            body: config.body,
            headers: config.headers,
            cookies: config.cookies,
            encoding: config.encoding,
            priority: config.priority,
            dont_filter: config.dont_filter
        };

        var msg = spider.sendFromResponseRequest(expected_msg.url, function(){},
                                                expected_msg.from_response_request, config);

        assert.deepEqual(JSON.parse(msg), expected_msg);
    });

    it('register the callback', function(){
        var responseId = spider._requestId;
        var callback = function() {};

        var msg = spider.sendFromResponseRequest('http://example.com', callback, {});
        assert.equal(spider.responseMapping[responseId], callback);
    })
});
