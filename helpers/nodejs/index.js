var spider = module.exports = {

    createSpider: function() {
    },

    closeSpider: function() {
    },

    sendLog: function() {
    },

    sendRequest: function() {
    },

    sendFromResponseRequest: function() {
    },

    runSpider: function(onException) {
        process.stdin.pipe(require('split')()).on('data', onLineReceive);
    }
}

var onException = function(msg) {
    if (self.exceptionHandler) {
        self.exceptionHandler(msg);
    }
    // TODO raise error
}

var checkStatus = function (msg) {

}

var onResponse = function (msg) {

}

var onError = function(msg) {

}

var mapping = {
    "ready": checkStatus,
    "response": onResponse,
    "exception": onException,
    "error": onError
}

var onLineReceive = function(line) {
    var msg = JSON.parse(line);
    var msg_type = msg.type;

    mapping[msg_type](msg);
}

// TODO remove the following closeSpider

spider.runSpider();
