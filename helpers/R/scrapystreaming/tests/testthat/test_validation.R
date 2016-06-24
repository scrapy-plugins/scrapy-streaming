library(testthat)
library(scrapystreaming)

context("Parameters validation")

test_that("create_spider ignroes callback if not necessary", {
    callback <- function(response) {}
    # must provide callback
    expect_error(create_spider("name", "http://example.com"))
    # valid usage
    expect_output(create_spider("name", "http://example.com", callback))
    # if no url, request not required
    expect_output(create_spider("name", character(0)))
})
