package org.scrapy.scrapystreaming.messages;


import java.util.List;

public class ReadyMessage extends Message {
    public final String type = "ready";
    public String status;

    public List<String> validator() {
        return null;
    }
}
