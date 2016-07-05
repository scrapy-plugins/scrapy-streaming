package org.scrapy.scrapystreaming.messages;

import java.util.HashMap;

public class FromResponseMessage {
    public String formname;
    public String formxpath;
    public String formcss;
    public Integer formnumber;
    public HashMap<String, String> formdata;
    public HashMap<String, String> clickdata;
    public Boolean dont_click;
}