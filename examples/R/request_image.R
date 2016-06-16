#!/usr/bin/env Rscript
suppressMessages(library(jsonlite))
suppressMessages(library(base64enc))

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

status <- get_json()

if (status$status != "ready") {
    stop("There is problem in the communication channel")
}

write_json('{
    "type": "spider",
    "name": "image",
    "start_urls": []
}')

write_json('{
    "type": "request",
    "id": "file",
    "url": "http://httpbin.org/image/png",
    "base64": true
}')

response <- get_json()

if (response["type"] == "exception") {
    stop("Failed to get content")
} else if (response["type"] == "response") {
    f <- file("outputs/image.png", "wb")
    base64decode(response$body, f)
    close(f)

    write_json('{"type": "log", "level": "debug", "message": "DONE"}')
}

write_json('{"type": "close"}')
