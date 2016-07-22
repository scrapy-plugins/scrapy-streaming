#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))

save_data <- function(response) {
    f <- file("outputs/fill_form.json")
    # serialize the extracted data and close the spider
    write(response$body, f)
    close(f);
    close_spider()
}

create_spider("form", character(0))
from_response_request <- data.frame(formdata = character(1))
from_response_request$formdata <- data.frame(custname = "Sample", custemail = "email@example.com")

send_from_response_request("http://httpbin.org/forms/post", save_data, from_response_request)

run_spider()
