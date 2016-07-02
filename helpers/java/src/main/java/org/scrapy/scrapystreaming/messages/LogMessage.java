package org.scrapy.scrapystreaming.messages;


import java.util.Arrays;
import java.util.List;

public class LogMessage extends Message {
    public final String type = "log";
    public String message;
    public String level;

    public LogMessage(String message, String level) {
        this.message = message;
        this.level = level;
    }

    public List<String> validator() {
        return Arrays.asList("type", "message", "level");
    }
}