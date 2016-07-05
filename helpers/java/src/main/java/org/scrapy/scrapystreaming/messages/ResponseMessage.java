package org.scrapy.scrapystreaming.messages;


import java.util.HashMap;
import java.util.List;

public class ResponseMessage extends Message {
    public final String type = "response";
    public String id;
    public String url;
    public HashMap<String, List<String>> headers;
    public Integer status;
    public String body;
    public HashMap<String, String> meta;
    public List<String> flags;

    public List<String> validator() {
        return null;
    }
}
