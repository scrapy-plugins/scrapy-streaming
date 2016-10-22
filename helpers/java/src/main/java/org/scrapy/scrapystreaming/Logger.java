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
     */
    public static void log(String message, LEVEL level) {
        try {
            new LogMessage(message, level.name()).sendMessage();
        } catch (SpiderException e) {
            // logger doesn't validate data
        }
    }

    /**
     * Print a critical message in the scrapy streaming logger
     * @param message message
     **/
    public static void critical(String message) {
        log(message, LEVEL.CRITICAL);
    }

    /**
     * Print a error message in the scrapy streaming logger
     * @param message message
     **/
    public static void error(String message) {
        log(message, LEVEL.ERROR);
    }

    /**
     * Print a warning in the scrapy streaming logger
     * @param message message
     **/
    public static void warning(String message) {
        log(message, LEVEL.WARNING);
    }

    /**
     * Print a info message in the scrapy streaming logger
     * @param message message
     **/
    public static void info(String message) {
        log(message, LEVEL.INFO);
    }

    /**
     * Print a debug message in the scrapy streaming logger
     * @param message message
     **/
    public static void debug(String message) {
        log(message, LEVEL.DEBUG);
    }
}

