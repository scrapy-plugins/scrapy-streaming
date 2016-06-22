#!/usr/bin/env Rscript
suppressMessages(library(scrapystreaming))

check_login <- function(response) {
    if (length(grep("Incorrect username or password", response$body)) > 0) {
        send_log("Invalid password", "error")
    } else {
        send_log("Logged!")
    }
    close_spider()
}

create_spider("login", character(0))
from_response_request <- data.frame(formdata = character(1))
from_response_request$formdata <- data.frame(login = "email@example.com", "password" = "password")

send_from_response_request("https://github.com/login", check_login, from_response_request)

run_spider()
