package org.scrapy.scrapystreaming.messages;


import java.util.List;
import java.util.Map;

public class ResponseMessage extends Message {
    public final String type = "response";
    public String id;
    public String url;
    public Map headers;
    public Integer status;
    public String body;
    public Map meta;
    public List<String> flags;

    public List<String> validator() {
        return null;
    }
}
