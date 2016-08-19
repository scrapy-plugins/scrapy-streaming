#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))
suppressMessages(library(rvest))


pending_requests <- 0
result <- list()

# function to get the initial page
response_parse <- function(response) {
    html <- read_html(response$body)

    for (a in html_nodes(html, "#subcategories-div > section > div > div.cat-item > a")) {
        # we count the number of requests using this var
        pending_requests <<- pending_requests + 1
        # open a new request to each subcategories
        send_request(sprintf("http://www.dmoz.org%s", html_attr(a, "href")), response_category)
    }
}

response_category <- function(response) {
    # this response is no longer pending
    pending_requests <<- pending_requests - 1

    html <- read_html(response$body)
    # get div with link and title
    for (div in html_nodes(html, "div.title-and-desc a")) {
        result[html_text(div, trim = TRUE)] <<- html_attr(div, "href")
    }

    # if finished all requests, we can close the spider
    if (pending_requests == 0) {
        f <- file("outputs/dmoz_data.json")
        # serialize the extracted data and close the spider
        write(toJSON(result), f)
        close(f)
        close_spider()
    }
}

create_spider("dmoz", "http://www.dmoz.org/Computers/Programming/Languages/Python/", response_parse)
run_spider()
