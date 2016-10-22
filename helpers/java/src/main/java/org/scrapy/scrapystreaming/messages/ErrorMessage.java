package org.scrapy.scrapystreaming.messages;


import java.util.List;

public class ErrorMessage extends Message {
    public final String type = "error";
    public String received_message;
    public String details;

    public List<String> validator() {
        return null;
    }
}
