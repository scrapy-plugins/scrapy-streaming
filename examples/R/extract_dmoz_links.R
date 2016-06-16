#!/usr/bin/env Rscript
suppressMessages(library(jsonlite))
suppressMessages(library(rvest))


std_in <- file("stdin")
open(std_in)

get_json <- function() {
    line <- readLines(std_in, n = 1)
    return(fromJSON(line))
}

write_json <- function(line) {
    line <- strwrap(line, width = 1000, simplify = TRUE)
    write(line, stdout())
    flush(stdout())
}

# get and check the communication channel status
status <- get_json()

if (status$status != "ready") {
    stop("There is problem in the communication channel")
}

# create the spider
write_json('{
    "type": "spider",
    "name": "dmoz",
    "start_urls": ["http://www.dmoz.org/Computers/Programming/Languages/Python/"]
}')

pending_requests <- 0
result <- list()

# function to get the initial page
response_parse <- function(response) {
    html <- read_html(response$body)

    for (a in html_nodes(html, "#subcategories-div > section > div > div.cat-item > a")) {
        # we count the number of requests using this var
        pending_requests <<- pending_requests + 1
        # open a new request to each subcategories
        write_json(sprintf('
            {
                "type": "request",
                "id": "category",
                "url": "http://www.dmoz.org%s"
            }
        ', html_attr(a, "href")))
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
        write_json('{"type": "close"}')
    }
}



while (TRUE) {
    msg <- get_json()

    # check if got a problem in the spider
    if (msg$type == "exception" || msg$type == "error") {
        stop("Something wrong")
    } else if (msg$type == "response") {
        # we check the id of the incoming response, and call a function
        # to extract the data from each page
        if (msg$id == "parse")
            response_parse(msg)
        else if (msg$id == "category")
            response_category(msg)
    }
}
