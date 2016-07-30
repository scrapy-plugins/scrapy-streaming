#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))

save_data <- function(response) {
    f <- file("outputs/post.json")
    # serialize the extracted data and close the spider
    write(response$body, f)
    close(f);
    close_spider()
}

create_spider("post", character(0))
send_request("http://httpbin.org/post", save_data, method = "POST", body = "Post data")

run_spider()
