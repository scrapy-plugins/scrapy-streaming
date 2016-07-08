package org.scrapy.scrapystreaming.messages;

import java.util.HashMap;
import java.util.Map;

public class FromResponseMessage {
    public String formname;
    public String formxpath;
    public String formcss;
    public Integer formnumber;
    public Map formdata;
    public Map clickdata;
    public Boolean dont_click;
}