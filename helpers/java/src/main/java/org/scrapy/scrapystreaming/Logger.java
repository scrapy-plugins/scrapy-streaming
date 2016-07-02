package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.LogMessage;

public class Logger {

    public enum LEVEL {
        CRITICAL, ERROR, WARNING, INFO, DEBUG
    }

    public static void log(String message, LEVEL level) throws SpiderException {
        new LogMessage(message, level.name()).sendMessage();
    }

    public static void logCritical(String message) throws SpiderException {
        log(message, LEVEL.CRITICAL);
    }

    public static void logError(String message) throws SpiderException {
        log(message, LEVEL.ERROR);
    }

    public static void logWarning(String message) throws SpiderException {
        log(message, LEVEL.WARNING);
    }

    public static void logInfo(String message) throws SpiderException {
        log(message, LEVEL.INFO);
    }

    public static void logDebug(String message) throws SpiderException {
        log(message, LEVEL.DEBUG);
    }
}

