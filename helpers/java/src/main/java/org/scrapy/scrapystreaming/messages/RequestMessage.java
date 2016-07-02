package org.scrapy.scrapystreaming.messages;


import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

public class RequestMessage extends Message {
    public final String type = "request";
    public String id;
    public String url;
    public Boolean base64;
    public String method;
    public HashMap<String, String> meta;
    public String body;
    public HashMap<String, String> headers;
    public HashMap<String, String> cookies;
    public String encoding;
    public Integer priority;
    public Boolean dont_filter;

    public List<String> validator() {
        return Arrays.asList("id", "url");
    }
}
