package org.scrapy.scrapystreaming.messages;


public class LogMessage extends Message{
    public final String type = "log";
    public final String message;
    public final String level;

    public LogMessage(String message, String level) {
        this.message = message;
        this.level = level;
    }
}