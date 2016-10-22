package org.scrapy.scrapystreaming.messages;


import java.util.List;

public class CloseMessage extends Message {
    public final String type = "close";

    public List<String> validator() {
        return null;
    }
}
