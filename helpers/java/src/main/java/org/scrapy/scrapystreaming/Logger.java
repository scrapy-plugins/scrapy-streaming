package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.LogMessage;

/**
 * Helper class to handle log messages
 */
public class Logger {

    public enum LEVEL {
        CRITICAL, ERROR, WARNING, INFO, DEBUG
    }

    /**
     * Print a log message in the scrapy streaming logger
     * @param message message
     * @param level log level
     * @throws SpiderException
     */
    public static void log(String message, LEVEL level) throws SpiderException {
        new LogMessage(message, level.name()).sendMessage();
    }

    /**
     * Print a critical message in the scrapy streaming logger
     * @param message message
     **/
    public static void logCritical(String message) throws SpiderException {
        log(message, LEVEL.CRITICAL);
    }

    /**
     * Print a error message in the scrapy streaming logger
     * @param message message
     **/
    public static void logError(String message) throws SpiderException {
        log(message, LEVEL.ERROR);
    }

    /**
     * Print a warning in the scrapy streaming logger
     * @param message message
     **/
    public static void logWarning(String message) throws SpiderException {
        log(message, LEVEL.WARNING);
    }

    /**
     * Print a info message in the scrapy streaming logger
     * @param message message
     **/
    public static void logInfo(String message) throws SpiderException {
        log(message, LEVEL.INFO);
    }

    /**
     * Print a debug message in the scrapy streaming logger
     * @param message message
     **/
    public static void logDebug(String message) throws SpiderException {
        log(message, LEVEL.DEBUG);
    }
}

