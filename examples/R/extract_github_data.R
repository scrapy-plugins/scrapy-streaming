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
    "name": "github",
    "start_urls": ["https://github.com/scrapy-plugins"]
}')

pending_requests <- 0
result <- list()

# function to get the initial page
response_parse <- function(response) {
    html <- read_html(response$body)

    for (a in html_nodes(html, "h3.repo-list-name > a")) {
        # we count the number of requests using this var
        pending_requests <<- pending_requests + 1
        # open a new request to each subcategories
        write_json(sprintf('{
            "type": "request",
            "id": "repo",
            "url": "https://github.com%s"
        }
        ', html_attr(a, "href")))
    }
}

response_repo <- function(response) {
    # this response is no longer pending
    pending_requests <<- pending_requests - 1

    html <- read_html(response$body)
    # get the desired fields
    item <- list()

    item["title"] <- html_text(html_node(html, "h1.public strong a"), trim = TRUE)
    item["stars"] <- html_text(html_node(html, "a.social-count"), trim = TRUE)
    item["issues"] <- html_text(html_node(html, "span.counter"), trim = TRUE)
    item["pr"] <- html_text(html_node(html, "span.counter"), trim = TRUE)

    result[item$title] <<- toJSON(item)

    # if finished all requests, we can close the spider
    if (pending_requests == 0) {
        f <- file("outputs/github_data.json")
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
        else if (msg$id == "repo")
            response_repo(msg)
    }
}
