package org.scrapy.scrapystreaming.messages;


import java.util.List;

public class ExceptionMessage extends Message {
    public final String type = "exception";
    public String received_message;
    public String exception;

    public List<String> validator() {
        return null;
    }
}
