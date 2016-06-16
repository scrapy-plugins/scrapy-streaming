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

status <- get_json()

if (status["status"] != "ready") {
    stop("There is problem in the communication channel")
}

write_json('{
    "type": "spider",
    "name": "login",
    "start_urls": []
}')

write_json('{
    "type": "form_request",
    "id": "login",
    "url": "https://github.com/login",
    "form_request": {
        "formdata": {
            "login": "email@example.com",
            "password": "password"
        }
    }
}')

response <- get_json()

if (length(grep("Incorrect username or password", response["body"])) > 0) {
    write_json('{"type": "log", "level": "ERROR", "message": "Invalid password"}')
} else {
    write_json('{"type": "log", "level": "debug", "message": "DONE"}')
}
