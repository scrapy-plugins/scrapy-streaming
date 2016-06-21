#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))


status <- parse_input()
create_spider("status", character(0))

requests <- c(200, 201, 400, 404, 500)

for (code in requests) {
    send_request(sprintf("http://httpbin.org/status/%s", code), function(r) {})
}

pending_requests <- length(requests)
results <- list()

while (pending_requests) {
    msg <- parse_input()
    # analyze the responses

    if (msg["type"] == "exception") {
        sent_message <- fromJSON(msg$received_message)
        results[sent_message$url] <- FALSE
    } else {
        results[msg$url] <- TRUE
    }

    pending_requests <- pending_requests - 1
}

f <- file("outputs/response_status.json")
write(toJSON(results), f)
close(f)
