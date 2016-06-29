package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.messages.LogMessage;

public class Logger {

    public enum LEVEL {
        CRITICAL, ERROR, WARNING, INFO, DEBUG
    }

    public static void log(String message, LEVEL level) {
        new LogMessage(message, level.name()).sendMessage();
    }

    public static void logCritical(String message) {
        log(message, LEVEL.CRITICAL);
    }

    public static void logError(String message) {
        log(message, LEVEL.ERROR);
    }

    public static void logWarning(String message) {
        log(message, LEVEL.WARNING);
    }

    public static void logInfo(String message) {
        log(message, LEVEL.INFO);
    }

    public static void logDebug(String message) {
        log(message, LEVEL.DEBUG);
    }
}

