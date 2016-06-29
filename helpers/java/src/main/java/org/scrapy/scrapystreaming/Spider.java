package org.scrapy.scrapystreaming;

import org.scrapy.scrapystreaming.messages.CloseMessage;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.scrapy.scrapystreaming.messages.SpiderMessage;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public abstract class Spider {
    public String name = "ExternalSpider";
    public List<String> start_urls = new ArrayList<String>(0);
    public List<String> allowed_domains;
    public HashMap<String, String> custom_settings;

    public void start() {
        new SpiderMessage(name, start_urls, allowed_domains, custom_settings).sendMessage();
    }

    public void close() {
        new CloseMessage().sendMessage();
    }

    public abstract void parse(ResponseMessage response);
}
