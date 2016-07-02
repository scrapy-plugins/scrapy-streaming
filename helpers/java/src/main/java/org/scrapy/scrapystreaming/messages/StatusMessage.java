package org.scrapy.scrapystreaming.messages;


import java.util.List;

public class StatusMessage extends Message {
    public final String type = "status";
    public String status;

    public List<String> validator() {
        return null;
    }
}
