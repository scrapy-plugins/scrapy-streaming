#!/usr/bin/env Rscript
suppressMessages(library(jsonlite))

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

if (status["status"] != "ready") {
    stop("There is problem in the communication channel")
}

# create the spider
write_json('{
    "type": "spider",
    "name": "status",
    "start_urls": []
}')

# open requests to test the http response
requests <- c(200, 201, 400, 404, 500)

for (code in requests) {
    # open each request
    write_json(sprintf('
        {
            "type": "request",
            "id": "%s",
            "url": "http://httpbin.org/status/%s"
        }', code, code)
    )
}

pending_requests <- length(requests)

results <- list()

while (pending_requests) {
    msg <- get_json()
    # analyze the responses

    if (msg["type"] == "exception") {
        sent_message <- fromJSON(msg$received_message)
        results$sent_message["id"] <- FALSE
    } else {
        results$msg["id"] <- TRUE
    }
    pending_requests <- pending_requests - 1
}

f <- file("outputs/response_status.json")
write(toJSON(results), f)
close(f)

write_json('{"type": "log", "level": "debug", "message": "DONE"}')
write_json('{"type": "close"}')
