#' @import jsonlite
library(jsonlite)

streaming.env <- new.env()
streaming.env$response_mapping = c()
streaming.env$request_id <- 1
streaming.env$std_in <- NULL

write_json <- function(json) {
    line <- strwrap(json, width = 100000, simplify = TRUE)
    write(line, stdout())
    flush(stdout())
}

gen_json <- function(obj) {
    json <- toJSON(obj)
    json <- substr(json, 2, nchar(json) - 1)
    return(json)
}

throw_error <- function(msg) {
    write(msg$received_message, stderr())
    stop(msg$details)
}

throw_exception <- function(msg) {
    write(msg$received_message, stderr())
    stop(msg$exception)
}

call_response <- function(msg) {
    streaming.env$response_mapping[[msg$id]](msg)
}

check_status <- function(msg) {
    if (msg$status != "ready") {
        stop("There is a problem in the communication channel")
    }
}

streaming.env$mapping <- list("error" = throw_error, "exception" = throw_error, "response" = call_response, "ready" = check_status)

#' Create and run a Spider
#'
#' Check the ScrapyStreaming and Scrapy documentations for more information about these parameters.
#'
#' @param name The name of the spider [character]
#' @param start_urls vector with initial urls [vector of character]
#' @param callback the function to handle the response callback from start_urls requests,
#'        must receive one parameter ``response`` that is a data.frame with the response data [function]
#' @param allowed_domains vector with allowed domains (optional) [vector of character]
#' @param custom_settings custom scrapy settings (optional) [data.frame]
#' @examples
#' parse <- function(response) {
#'  print(response$headers)
#' }
#'
#' create_spider(name = "sample",
#'               start_urls = "http://example.com",
#'               allowed_domains = c("example.com", "dmoz.org"),
#'               callback = parse,
#'               custom_settings = data.frame("SOME_SETTING" = "some value"))
#'
#' @export
create_spider <- function(name, start_urls, callback, allowed_domains, custom_settings){
    stopifnot(is.character(name) && length(name) == 1)
    stopifnot(is.character(start_urls) && is.vector(start_urls))
    if (length(start_urls) > 0) {
        stopifnot(is.function(callback))
        streaming.env$response_mapping["parse"] <- list(callback)
    } else {
        callback <- NULL;
    }
    if (missing(allowed_domains))
        allowed_domains = c()
    else
        stopifnot(is.character(allowed_domains) && is.vector(allowed_domains))
    if (missing(custom_settings))
        custom_settings = c()
    else
        stopifnot(is.data.frame(custom_settings))

    spider <- data.frame(type = "spider", name = name)
    spider$start_urls <- list(start_urls)
    if (length(allowed_domains) > 0)
        spider$allowed_domains <- list(allowed_domains)
    if (length(custom_settings) > 0)
        spider$custom_settings <- custom_settings

    json <- gen_json(spider)
    write_json(json)
}

#' Send a message to close the spider
#'
#' @return the json message sent to stdout
#' @export
close_spider <- function() {
    msg <- data.frame(type = "close")

    json <- gen_json(msg)
    write_json(json)
    return(json)
}

#' Runs the spider
#'
#' @export
run_spider <- function() {
    while (TRUE) {
        handle()
    }
}



#' Create an open a new request
#'
#' Check the ScrapyStreaming and Scrapy documentations for more information about these parameters.
#'
#' @param url request url [character]
#' @param callback the function to handle the response callback,
#'        must receive one parameter ``response`` that is a data.frame with the response data [function]
#' @param base64 bool, if True, the response body will be encoded with base64 (optional) [logical]
#' @param method request method (optional) [character]
#' @param meta metadata to the request (optional) [data.frame]
#' @param body the request body (optional) [character]
#' @param headers request headers (optional) [data.frame]
#' @param cookies request cookies  (optional) [data.frame]
#' @param encoding request encoding  (optional) [character]
#' @param priority request priority  (optional) [numeric]
#' @param dont_filter indicates that this request should not be filtered by the scheduler (optional) [logical]
#' @examples
#' my_callback <- function (response) {
#'  print(response)
#' }
#' send_request("http://example.com", my_callback)
#'
#' @export
send_request <- function(url, callback, base64, method, meta, body, headers, cookies, encoding, priority, dont_filter) {
    request <- data.frame(type = "request")

    stopifnot(is.character(url) && length(url) == 1)
    stopifnot(is.function(callback))
    request$url <- url
    request$id <- as.character(streaming.env$request_id)

    streaming.env$response_mapping[toString(streaming.env$request_id)] <- list(callback)
    streaming.env$request_id <- streaming.env$request_id + 1

    if (missing(base64)) {
        base64 <- NA
    } else {
        stopifnot(is.logical(base64) && length(base64) == 1)
        request$base64 <- base64
    }
    if (missing(method)) {
        method <- NA
    } else {
        stopifnot(is.character(method) && length(method) == 1)
        request$method <- method
    }
    if (missing(meta)) {
        meta <- NA
    } else {
        stopifnot(is.data.frame(meta))
        request$meta <- meta
    }
    if (missing(body)) {
        body <- NA
    } else {
        stopifnot(is.character(body) && length(body) == 1)
        request$body <- body
    }
    if (missing(headers)) {
        headers <- NA
    } else {
        stopifnot(is.data.frame(headers))
        request$headers <- headers
    }
    if (missing(cookies)) {
        cookies <- NA
    } else {
        stopifnot(is.data.frame(cookies))
        request$cookies <- cookies
    }
    if (missing(encoding)) {
        encoding <- NA
    } else {
        stopifnot(is.character(encoding) && length(encoding) == 1)
        request$encoding <- encoding
    }
    if (missing(priority)) {
        priority <- NA
    } else {
        stopifnot(is.numeric(priority) && length(priority) == 1)
        request$priority <- priority
    }
    if (missing(dont_filter)) {
        dont_filter <- NA
    } else {
        stopifnot(is.logical(dont_filter) && length(dont_filter) == 1)
        request$dont_filter <- dont_filter
    }

    json <- gen_json(request)
    write_json(json)
}

#' Create an open a new request
#'
#' Create an open a new request and uses its response to open a new request using scrapy's FormRequest.from_response and ``form_request`` data.
#' Check the ScrapyStreaming and Scrapy documentations for more information about these parameters.
#'
#' @param url request url [character]
#' @param callback the function to handle the response callback,
#'        must receive one parameter ``response`` that is a data.frame with the response data [function]
#'
#' @param from_response_request data to the new request. May contain fields to the request and to the form. [data.frame]
#' @param base64 bool, if True, the response body will be encoded with base64 (optional) [logical]
#' @param method request method (optional) [character]
#' @param meta metadata to the request (optional) [data.frame]
#' @param body the request body (optional) [character]
#' @param headers request headers (optional) [data.frame]
#' @param cookies request cookies  (optional) [data.frame]
#' @param encoding request encoding  (optional) [character]
#' @param priority request priority  (optional) [numeric]
#' @param dont_filter indicates that this request should not be filtered by the scheduler (optional) [logical]
#' @examples
#' my_callback <- function (response) {
#'  print(response)
#' }
#'
#' # first we defined the dataframe structure
#' from_response_request <- data.frame(formcss = character(1), formdata = character(1))
#'
#' # then we put the dataframe data
#' from_response_request$formcss <- "#login_form"
#' from_response_request$formdata <- data.frame(user = "admin", pass = "1")
#'
#' send_from_response_request("http://example.com", my_callback, from_response_request)
#'
#' @export
send_from_response_request <- function(url, callback, from_response_request, base64, method, meta, body, headers, cookies, encoding, priority, dont_filter) {
    request <- data.frame(type = "from_response_request")

    stopifnot(is.character(url) && length(url) == 1)
    stopifnot(is.function(callback))
    stopifnot(is.data.frame(from_response_request))
    request$url <- url
    request$id <- as.character(streaming.env$request_id)
    request$from_response_request <- from_response_request

    streaming.env$response_mapping[toString(streaming.env$request_id)] <- list(callback)
    streaming.env$request_id <- streaming.env$request_id + 1

    ####################
    # request validation
    ####################

    if (missing(base64)) {
        base64 <- NA
    } else {
        stopifnot(is.logical(base64) && length(base64) == 1)
        request$base64 <- base64
    }
    if (missing(method)) {
        method <- NA
    } else {
        stopifnot(is.character(method) && length(method) == 1)
        request$method <- method
    }
    if (missing(meta)) {
        meta <- NA
    } else {
        stopifnot(is.data.frame(meta))
        request$meta <- meta
    }
    if (missing(body)) {
        body <- NA
    } else {
        stopifnot(is.character(body) && length(body) == 1)
        request$body <- body
    }
    if (missing(headers)) {
        headers <- NA
    } else {
        stopifnot(is.data.frame(headers))
        request$headers <- headers
    }
    if (missing(cookies)) {
        cookies <- NA
    } else {
        stopifnot(is.data.frame(cookies))
        request$cookies <- cookies
    }
    if (missing(encoding)) {
        encoding <- NA
    } else {
        stopifnot(is.character(encoding) && length(encoding) == 1)
        request$encoding <- encoding
    }
    if (missing(priority)) {
        priority <- NA
    } else {
        stopifnot(is.numeric(priority) && length(priority) == 1)
        request$priority <- priority
    }
    if (missing(dont_filter)) {
        dont_filter <- NA
    } else {
        stopifnot(is.logical(dont_filter) && length(dont_filter) == 1)
        request$dont_filter <- dont_filter
    }

    ##################################
    # from_response_request validation
    ##################################

    # request
    if (!is.null(from_response_request$method))
        stopifnot(is.character(from_response_request$method) && length(from_response_request$method) == 1)
    if (!is.null(from_response_request$meta))
        stopifnot(is.data.frame(from_response_request$meta))
    if (!is.null(from_response_request$body))
        stopifnot(is.character(from_response_request$body) && length(from_response_request$body) == 1)
    if (!is.null(from_response_request$headers))
        stopifnot(is.data.frame(from_response_request$headers))
    if (!is.null(from_response_request$cookies))
        stopifnot(is.data.frame(from_response_request$cookies))
    if (!is.null(from_response_request$encoding))
        stopifnot(is.character(from_response_request$encoding) && length(from_response_request$encoding) == 1)
    if (!is.null(from_response_request$priority))
        stopifnot(is.numeric(from_response_request$priority) && length(from_response_request$priority) == 1)
    if (!is.null(from_response_request$dont_filter))
        stopifnot(is.logical(from_response_request$dont_filter) && length(from_response_request$dont_filter) == 1)

    # from_response
    if (!is.null(from_response_request$formname))
        stopifnot(is.character(from_response_request$formname) && length(from_response_request$formname) == 1)
    if (!is.null(from_response_request$formxpath))
        stopifnot(is.character(from_response_request$formxpath) && length(from_response_request$formxpath) == 1)
    if (!is.null(from_response_request$formcss))
        stopifnot(is.character(from_response_request$formcss) && length(from_response_request$formcss) == 1)
    if (!is.null(from_response_request$formnumber))
        stopifnot(is.character(from_response_request$formnumber) && length(from_response_request$formnumber) == 1)
    if (!is.null(from_response_request$formdata))
        stopifnot(is.data.frame(from_response_request$formdata))
    if (!is.null(from_response_request$clickdata))
        stopifnot(is.data.frame(from_response_request$clickdata))
    if (!is.null(from_response_request$dont_click))
        stopifnot(is.logical(from_response_request$dont_click) && length(from_response_request$dont_click) == 1)

    json <- gen_json(request)
    write_json(json)
}

#' Send a log to Scrapy Streaming
#'
#' @param message the log message
#' @param level log level. Must be one of 'CRITICAL', 'ERROR', 'WARNING', 'DEBUG', and 'INFO', defaults to DEBUG
#'
#' @examples
#' send_log("log works!")
#' send_log("logging error :(", "error")
#'
#' @export
send_log <- function(message, level) {
    stopifnot(is.character(message) && length(message) == 1)
    if (missing(level))
        level <- "DEBUG"
    stopifnot(is.character(level) && length(level) == 1)

    level <- toupper(level)
    if (!is.element(level, c("CRITICAL", "ERROR", "WARNING", "DEBUG", "INFO"))) {
        stop("Log level must be one of 'CRITICAL', 'ERROR', 'WARNING', 'DEBUG', and 'INFO'")
    }

    log <- data.frame(type = "log", message = message, level = level)

    json <- gen_json(log)
    write_json(json)
}

#' Read and returns a stdin line
#'
#' @param raw if TRUE, returns the raw input line. If FALSE (the default), parse it using jsonlite::fromJSON
#' @param ... extra arguments to jsonlite::fromJSON
#'
#' @return the json message sent to stdout
#' @export
parse_input <- function(raw, ...) {
    if (missing(raw)) {
        raw <- FALSE
    }

    if (is.null(streaming.env$std_in)) {
        streaming.env$std_in <- file("stdin")
        open(streaming.env$std_in)
    }

    line <- readLines(streaming.env$std_in, n = 1)
    if (raw) {
        return(line)
    } else {
        if (length(line) == 0) {
            # in case of empty stdin, igores it
            return(line)
        } else {
            return(fromJSON(line, ...))
        }
    }
}

#' Handles the input message
#'
#' @param execute if TRUE (the default) will execute the message as follows:
#'                * ready: if the status is ready, continue the
#'                * response: call the callback with the message as the first parameter
#'                * error: stop the execution of the process and show the spider error
#'                * exception: stop the execution of the process and show the scrapy exception
#' @export
handle <- function(execute) {
    if (missing(execute)) {
        execute <- TRUE
    }
    msg <- parse_input()
    if (execute) {
        streaming.env$mapping[[msg$type]](msg)
    } else {
        return(msg)
    }

}
