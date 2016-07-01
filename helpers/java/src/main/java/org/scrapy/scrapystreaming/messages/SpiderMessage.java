package org.scrapy.scrapystreaming.messages;


import java.util.List;
import java.util.HashMap;

public class SpiderMessage extends Message {
    public final String type = "spider";
    public String name;
    public List<String> start_urls;
    public List<String> allowed_domains;
    public HashMap<String, String> custom_settings;

    public SpiderMessage(String name, List<String> start_urls, List<String> allowed_domains,
                         HashMap<String, String> custom_settings) {
        this.name = name;
        this.start_urls = start_urls;
        this.allowed_domains = allowed_domains;
        this.custom_settings = custom_settings;
    }
}
