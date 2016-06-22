#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))
suppressMessages(library(base64enc))

save_file <- function(response) {
    f <- file("outputs/image.png", "wb")
    base64decode(response$body, f)
    close(f)
    close_spider()
}
create_spider("image", character(0))
send_request("http://httpbin.org/image/png", save_file, TRUE)

run_spider()
