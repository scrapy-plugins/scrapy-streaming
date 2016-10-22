package org.scrapy.scrapystreaming.messages;



import java.util.*;

public class SpiderMessage extends Message {
    public final String type = "spider";
    public String name = "ExternalSpider";
    public List<String> start_urls = new ArrayList<String>(0);
    public List<String> allowed_domains;
    public Map custom_settings;

    public List<String> validator() {
        return Arrays.asList("type", "name", "start_urls");
    }
}
