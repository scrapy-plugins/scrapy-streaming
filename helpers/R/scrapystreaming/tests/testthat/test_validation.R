library(testthat)
library(scrapystreaming)

context("Parameters validation")

callback <- function(response) {}

test_that("create_spider validate all parameters", {
    # must provide callback
    expect_error(create_spider("name", "http://example.com"))
    # valid usage
    expect_output(create_spider("name", "http://example.com", callback))
    # if no url, request not required
    expect_output(create_spider("name", character(0)))
    # wrong allowed_domains param
    expect_error(create_spider("name", "http://example.com", callback, allowed_domains = data.frame(domain = "example.com")))
    # pass allowed_domains
    expect_output(create_spider("name", "http://example.com", callback, allowed_domains = c("example.com", "example.com.br")))
    # wrong custom_settings param
    expect_error(create_spider("name", "http://example.com", callback, custom_settings = c("example.com")))
    # pass custom_settings param
    expect_output(create_spider("name", "http://example.com", callback, custom_settings = data.frame(a = "a", b = "b")))
})

test_that("send_request validate all parameters", {
    # invalid base64
    expect_error(send_request("http://example.com", callback, base64 = 1))
    # pass base64
    expect_output(send_request("http://example.com", callback, TRUE))
    # invalid method
    expect_error(send_request("http://example.com", callback, method = c("GET", "POST")))
    # pass method
    expect_output(send_request("http://example.com", callback, method = "POST"))
    # invalid meta
    expect_error(send_request("http://example.com", callback, meta = list(a = 1, b = 2)))
    # pass meta
    expect_output(send_request("http://example.com", callback, meta = data.frame(a = 1, b = 2)))
    # invalid body
    expect_error(send_request("http://example.com", callback, body = NULL))
    # pass body
    expect_output(send_request("http://example.com", callback, body = "content"))
    # invalid headers
    expect_error(send_request("http://example.com", callback, headers = c("content-header", "content-type")))
    # pass headers
    expect_output(send_request("http://example.com", callback, headers = data.frame(a = 1, b = 2)))
    # invalid cookies
    expect_error(send_request("http://example.com", callback, cookies = c("a", "b")))
    # pass cookies
    expect_output(send_request("http://example.com", callback, cookies = data.frame(a = 1, b = "aa")))
    # invalid encoding
    expect_error(send_request("http://example.com", callback, encoding = 1))
    # pass encoding
    expect_output(send_request("http://example.com", callback, encoding = "utf8"))
    # invalid priority
    expect_error(send_request("http://example.com", callback, priority = "high"))
    # pass priority
    expect_output(send_request("http://example.com", callback, priority = 1))
    # invalid dont_filter
    expect_error(send_request("http://example.com", callback, dont_filter = 1))
    # pass dont_filter
    expect_output(send_request("http://example.com", callback, dont_filter = TRUE))
})

test_that("send_from_response_request validate all parameters", {
    ### testing initial request ###
    data <- data.frame(formname = character(1))
    data$formname <- "name"
    # invalid base64
    expect_error(send_from_response_request("http://example.com", callback, data,  base64 = 1))
    # pass base64
    expect_output(send_from_response_request("http://example.com", callback, data,  TRUE))
    # invalid method
    expect_error(send_from_response_request("http://example.com", callback, data,  method = c("GET", "POST")))
    # pass method
    expect_output(send_from_response_request("http://example.com", callback, data,  method = "POST"))
    # invalid meta
    expect_error(send_from_response_request("http://example.com", callback, data,  meta = list(a = 1, b = 2)))
    # pass meta
    expect_output(send_from_response_request("http://example.com", callback, data,  meta = data.frame(a = 1, b = 2)))
    # invalid body
    expect_error(send_from_response_request("http://example.com", callback, data,  body = NULL))
    # pass body
    expect_output(send_from_response_request("http://example.com", callback, data,  body = "content"))
    # invalid headers
    expect_error(send_from_response_request("http://example.com", callback, data,  headers = c("content-header", "content-type")))
    # pass headers
    expect_output(send_from_response_request("http://example.com", callback, data,  headers = data.frame(a = 1, b = 2)))
    # invalid cookies
    expect_error(send_from_response_request("http://example.com", callback, data,  cookies = c("a", "b")))
    # pass cookies
    expect_output(send_from_response_request("http://example.com", callback, data,  cookies = data.frame(a = 1, b = "aa")))
    # invalid encoding
    expect_error(send_from_response_request("http://example.com", callback, data,  encoding = 1))
    # pass encoding
    expect_output(send_from_response_request("http://example.com", callback, data,  encoding = "utf8"))
    # invalid priority
    expect_error(send_from_response_request("http://example.com", callback, data,  priority = "high"))
    # pass priority
    expect_output(send_from_response_request("http://example.com", callback, data,  priority = 1))
    # invalid dont_filter
    expect_error(send_from_response_request("http://example.com", callback, data,  dont_filter = 1))
    # pass dont_filter
    expect_output(send_from_response_request("http://example.com", callback, data,  dont_filter = TRUE))

    ### test from_respose parameter ###

    # testing from_response_request$method
    data <- data.frame(method = character(1))
    data$method <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$method <- "GET"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$meta
    data <- data.frame(meta = character(1))
    data$meta <- "data"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$meta <- data.frame(a = 1, b = 2)
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$body
    data <- data.frame(body = character(1))
    data$body <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$body <- "body content"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$eaders
    data <- data.frame(headers = character(1))
    data$headers <- "content-type"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$headers <- data.frame(a = 1, b = 2)
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$cookies
    data <- data.frame(cookies = character(1))
    data$cookies <- "aaa"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$cookies <- data.frame(a = 1, b = 2)
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$encoding
    data <- data.frame(encoding = character(1))
    data$encoding <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$encoding <- "latin"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$priority
    data <- data.frame(priority = character(1))
    data$priority <- "hight"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$priority <- 2
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$dont_filter
    data <- data.frame(dont_filter = character(1))
    data$dont_filter <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$dont_filter <- FALSE
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$formname
    data <- data.frame(formname = character(1))
    data$formname <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$formname <- "name"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$formxpath
    data <- data.frame(formxpath = character(1))
    data$formxpath <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$formxpath <- "selector"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$formcss
    data <- data.frame(formcss = character(1))
    data$formcss <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$formcss <- "selector"
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$formnumber
    data <- data.frame(formnumber = character(1))
    data$formnumber <- "1"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$formnumber <- 1
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$formdata
    data <- data.frame(formdata = character(1))
    data$formdata <- "name = 1"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$formdata <- data.frame(name = 1)
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$clickdata
    data <- data.frame(clickdata = character(1))
    data$clickdata <- "x = 1"
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$clickdata <- data.frame(x = 1)
    expect_output(send_from_response_request("http://example.com", callback, data))
    # testing from_response_request$dont_click
    data <- data.frame(dont_click = character(1))
    data$dont_click <- 1
    expect_error(send_from_response_request("http://example.com", callback, data))
    data$dont_click <- TRUE
    expect_output(send_from_response_request("http://example.com", callback, data))

    # wrong parameters
    data <- data.frame(x = character(1))
    data$x <- 1
    expect_error(send_from_response_request("http://example.com", callback, data), "x is not a valid from_response_request parameter")
})
