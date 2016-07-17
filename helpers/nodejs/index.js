var spider = module.exports = {

    exceptionHandler: null,
    responseMapping: {},
    _requestId: 1,

    /**
     * Create the spider
     *
     * @param  {string}   name            name of the spider
     * @param  {array}    startUrls      list of initial urls
     * @param  {Function} callback        callback to handle the responses from startUrls
     * @param  {array}    allowedDomains list of allowed domains
     * @param  {object}   customSettings custom settings to be used in Scrapy
     *
     * @return {string}                   json message written in the process stdout
     */
    createSpider: function(name, startUrls, callback, allowedDomains, customSettings) {
        // required fields
        _isDefined(name, 'name');
        _isDefined(startUrls, 'startUrls');
        _isDefined(callback, 'callback');

        // validation
        _validateType(name, 'string', 'name');
        _validateType(callback, 'function', 'callback');
        customSettings && _validateType(customSettings, 'object', 'customSettings');

        if (startUrls) {
            if (startUrls.constructor !== Array) {
                throw new Error('startUrls parameter must be an array. Received: '
                                + typeof startUrls);
            }
        }

        if (allowedDomains) {
            if (allowedDomains.constructor !== Array) {
                throw new Error('allowedDomains parameter must be an array. Received: '
                                + typeof allowedDomains);
            }
        }

        if (customSettings) {
            if (allowedDomains.constructor !== Array) {
                throw new Error('allowedDomains parameter must be an array. Received: '
                                + typeof allowedDomains);
            }
        }

        this.responseMapping['parse'] = callback;

        var msg = {
            type: 'spider',
            name: name,
            start_urls: startUrls || undefined,
            allowed_domains: allowedDomains || undefined,
            custom_settings: customSettings || undefined
        };

        return writeJson(msg);
    },

    closeSpider: function() {
        var msg = {
            'type': 'close'
        };

        return writeJson(msg);
    },

    /**
     * Send a log message to the Scrapy Streaming, using the log message
     *
     * @param  {string} message log message
     * @param  {string} level   log level, must be one of 'CRITICAL', 'ERROR', 'WARNING', 'INFO', and 'DEBUG'
     *
     * @return {string}         json message written in the process stdout
     */
    sendLog: function(message, level) {
        // required
        _isDefined(message, 'message');
        _isDefined(level, 'level');
        // validation
        _validateType(message, 'string', 'message');
        _validateType(level, 'string', 'level');

        var acceptedLevels = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'];
        level = level.toUpperCase();
        if (acceptedLevels.indexOf(level) === -1) {
            throw new Error('Invalid log level. Must be one of ' +
                            '\'CRITICAL\', \'ERROR\', \'WARNING\', \'INFO\', \'DEBUG\'');
        }

        var msg = {
            type: 'log',
            message: message,
            level: level
        };

        return writeJson(msg);
    },

    /**
     * Opens a new request
     *
     * @param  {string}   url        request url
     * @param  {Function} callback   response callback
     * @param  {boolean}  base64     if true, converts the response body to base64. (optional)
     * @param  {string}   method     request method (optional)
     * @param  {object}   meta       request extra data (optional)
     * @param  {string}   body       request body (optional)
     * @param  {object}   headers    request headers (optional)
     * @param  {object}   cookies    rqeuest extra cookies (optional)
     * @param  {string}   encoding   default encoding (optional)
     * @param  {int}      priority   request priority  (optional)
     * @param  {boolean}   dontFilter if true, the request don't pass on the request duplicate filter (optional)
     *
     * @return {string}              json message written in the process stdout
     */
    sendRequest: function(url, callback, base64, method, meta, body, headers, cookies, encoding, priority, dontFilter) {
        // required fields
        _isDefined(url, 'url');
        _isDefined(callback, 'callback');

        // validation
        _validateType(url, 'string', 'url');
        _validateType(callback, 'function', 'callback');
        base64 && _validateType(base64, 'boolean', 'base64');
        method && _validateType(method, 'string', 'method');
        meta && _validateType(meta, 'object', 'meta');
        body && _validateType(body, 'string', 'body');
        headers && _validateType(headers, 'object', 'headers');
        cookies && _validateType(cookies, 'object', 'cookies');
        encoding && _validateType(encoding, 'string', 'encoding');
        priority && _validateType(priority, 'number', 'priority');
        dontFilter && _validateType(dontFilter, 'boolean', 'dontFilter');

        this.responseMapping[this._requestId] = callback;

        var msg = {
            type: 'request',
            url: url,
            id: this._requestId,
            base64: base64 || undefined,
            method: method || undefined,
            meta: meta || undefined,
            body: body || undefined,
            headers: headers || undefined,
            cookies: cookies || undefined,
            encoding: encoding || undefined,
            priority: priority || undefined,
            dont_filter: dontFilter || undefined
        };

        this._requestId++;

        return writeJson(msg);
    },

    /**
     * Opens a new request
     *
     * @param  {string}   url        request url
     * @param  {Function} callback   response callback
     * @param  {fromResponseRequest} Creates a new request using the response
     * @param  {boolean}  base64     if true, converts the response body to base64. (optional)
     * @param  {string}   method     request method (optional)
     * @param  {object}   meta       request extra data (optional)
     * @param  {string}   body       request body (optional)
     * @param  {object}   headers    request headers (optional)
     * @param  {object}   cookies    rqeuest extra cookies (optional)
     * @param  {string}   encoding   default encoding (optional)
     * @param  {int}      priority   request priority  (optional)
     * @param  {boolean}   dontFilter if true, the request don't pass on the request duplicate filter (optional)
     *
     * @return {string}              json message written in the process stdout
     */
    sendFromResponseRequest: function(url, callback, fromResponseRequest, base64, method, meta, body, headers, cookies, encoding, priority, dontFilter) {
        // required fields
        _isDefined(url, 'url');
        _isDefined(callback, 'callback');
        _isDefined(fromResponseRequest, 'fromResponseRequest');

        // validation - request
        _validateType(url, 'string', 'url');
        _validateType(callback, 'function', 'callback');
        _validateType(fromResponseRequest, 'object', 'fromResponseRequest');
        base64 && _validateType(base64, 'boolean', 'base64');
        method && _validateType(method, 'string', 'method');
        meta && _validateType(meta, 'object', 'meta');
        body && _validateType(body, 'string', 'body');
        headers && _validateType(headers, 'object', 'headers');
        cookies && _validateType(cookies, 'object', 'cookies');
        encoding && _validateType(encoding, 'string', 'encoding');
        priority && _validateType(priority, 'number', 'priority');
        dontFilter && _validateType(dontFilter, 'boolean', 'dontFilter');

        // validation - fromResponseRequest

        fromResponseRequest.url && _validateType(fromResponseRequest.url, 'string', 'fromResponseRequest.url');
        fromResponseRequest.method && _validateType(fromResponseRequest.method, 'string', 'fromResponseRequest.method');
        fromResponseRequest.meta && _validateType(fromResponseRequest.meta, 'object', 'fromResponseRequest.meta');
        fromResponseRequest.body && _validateType(fromResponseRequest.body, 'string', 'fromResponseRequest.body');
        fromResponseRequest.headers && _validateType(fromResponseRequest.headers, 'object', 'fromResponseRequest.headers');
        fromResponseRequest.cookies && _validateType(fromResponseRequest.cookies, 'object', 'fromResponseRequest.cookies');
        fromResponseRequest.encoding && _validateType(fromResponseRequest.encoding, 'string', 'fromResponseRequest.encoding');
        fromResponseRequest.priority && _validateType(fromResponseRequest.priority, 'number', 'fromResponseRequest.priority');
        fromResponseRequest.dont_filter && _validateType(fromResponseRequest.dont_filter, 'boolean', 'fromResponseRequest.dont_filter');

        fromResponseRequest.formname && _validateType(fromResponseRequest.formname, 'string', 'fromResponseRequest.formname');
        fromResponseRequest.formxpath && _validateType(fromResponseRequest.formxpath, 'string', 'fromResponseRequest.formxpath');
        fromResponseRequest.formcss && _validateType(fromResponseRequest.formcss, 'string', 'fromResponseRequest.formcss');
        fromResponseRequest.formnumber && _validateType(fromResponseRequest.formnumber, 'number', 'fromResponseRequest.formnumber');
        fromResponseRequest.formdata && _validateType(fromResponseRequest.formdata, 'object', 'fromResponseRequest.formdata');
        fromResponseRequest.clickdata && _validateType(fromResponseRequest.clickdata, 'object', 'fromResponseRequest.clickdata');
        fromResponseRequest.dont_click && _validateType(fromResponseRequest.dont_click, 'boolean', 'fromResponseRequest.dont_click');

        this.responseMapping[this._requestId] = callback;

        var msg = {
            type: 'from_response_request',
            url: url,
            id: this._requestId,
            from_response_request: fromResponseRequest,
            base64: base64 || undefined,
            method: method || undefined,
            meta: meta || undefined,
            body: body || undefined,
            headers: headers || undefined,
            cookies: cookies || undefined,
            encoding: encoding || undefined,
            priority: priority || undefined,
            dont_filter: dontFilter || undefined
        };

        this._requestId++;

        return writeJson(msg);
    },

    /**
     * Starts the spider execution. This will bind the process stdin to read data
     * from Scrapy Streaming, and process each message received.
     *
     * If you want to handle the exceptions generated by Scrapy, pass a function that receives a single parameter as an argument.
     *
     * By default, any exception will stop the spider execution and throw an Error.
     * @param  {Function} exceptionHandler function to handle exceptions. Must receive a single parameter, the received json with the exception. (optional)
     */
    runSpider: function(exceptionHandler) {
        if (exceptionHandler !== undefined) {
            _validateType(exceptionHandler, 'function', 'exceptionHandler');
            spider.exceptionHandler = exceptionHandler;
        }
        process.stdin.pipe(require('split')()).on('data', onLineReceive);
    }
};

/**
 * Function that receives the exception message.
 *
 * If there is a exceptionHandler registered in the spider, it will dispatch the exception.
 * Otherwise, the script will throw an exception.
 * @param  {object} msg received exception message
 */
var onException = function (msg) {
    // uses the exceptionHandler if available
    if (spider.exceptionHandler) {
        spider.exceptionHandler(msg);
    } else {

        throw new Error ('There is a problem in the Scrapy Streaming: \n\tReceived message: ' +
                         msg.received_message + '. \n\tError: ' + msg.exception + '\n\n');
    }
};

/**
 * Validate if the spider connected successfuly with the Scrapy Streaming
 *
 * @param  {object} msg received ready message
 */
var checkStatus = function (msg) {
    if (msg.status !== 'ready') {
        throw new Error ('There is a problem in the communication channel: ' + msg.status);
    }
};

/**
 * Receives the response from a request. Call the callback function, sending
 * the received response
 * @param  {object} msg response. It will be sent to the callback function
 */
var onResponse = function (msg) {
    spider.responseMapping[msg.id](msg);
};

/**
 * Receives the Error message. This message implies that there is a problem in the spider
 * source code.
 *
 * The spider execution will stop, and more details will be visible in the Scrapy Streaming logger.
 * @param  {object} msg error message
 */
var onError = function (msg) {
    throw new Error ('There is a problem in the Spider: \n\tReceived message: ' +
                     msg.received_message + '. \n\tError: ' + msg.details + '\n\n');
};

var mapping = {
    'ready': checkStatus,
    'response': onResponse,
    'exception': onException,
    'error': onError
};

/**
 * Receives a json in a single line, parse it, and call the respective message handler.
 *
 * @param  {string} line string with the json message sent by Scrapy Streaming.
 */
var onLineReceive = function(line) {
    var msg = JSON.parse(line);
    var msg_type = msg.type;

    mapping[msg_type](msg);
};

/**
 * Converts a JS object to json and writes it to the process stdout
 * @param  {object} obj message to be sent
 * @return {string}     the string printed in the process stdout
 */
var writeJson = function(obj) {
    var json = JSON.stringify(obj);

    process.stdout.write(json + '\n');

    return json;
};

/**
 * Validate if a variable is defined, trows an exception if not.
 *
 * @param  {var} paramenter variable to be tested
 * @param  {string} name       verbose name of the variable
 *
 * @return {boolean}            true, if is defined. Otherwise, throws an exception
 */
var _isDefined = function(paramenter, name) {
    if (paramenter === undefined) {
        throw new Error('Error: missing ' + name + ' parameter');
    }
    return true;
};

/**
 * Validates the type of a variable
 *
 * @param  {var}    variable     variable to be tested
 * @param  {string} expectedType name of the expected type
 * @param  {string} name         verbose name of the variable
 *
 * @return {boolean}             true if it the type if valid. Otherwise, throws an exception.
 */
var _validateType = function(variable, expectedType, name) {
    if (typeof variable !== expectedType) {
        throw new Error(name + ' parameter must be ' + expectedType + '. Received: '
                        + typeof variable);
    }
    return true;
};
