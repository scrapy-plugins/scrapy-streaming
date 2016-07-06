package org.scrapy.scrapystreaming;


import org.junit.Assert;
import org.junit.Test;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.LogMessage;



public class LoggerTest extends BaseStd {

    @Test
    public void log() throws SpiderException {
        for (Logger.LEVEL level: Logger.LEVEL.values()) {
            Logger.log("message", level);

            LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
            LogMessage logExpected = new LogMessage("message", level.name());
            out.reset();

            Assert.assertEquals(logExpected, logMessage);
        }
    }

    @Test
    public void logCritical() throws Exception {
        Logger.critical("critical");

        LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
        LogMessage logExpected = new LogMessage("critical", Logger.LEVEL.CRITICAL.name());

        Assert.assertEquals(logMessage, logExpected);
    }

    @Test
    public void logError() throws Exception {
        Logger.error("error");

        LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
        LogMessage logExpected = new LogMessage("error", Logger.LEVEL.ERROR.name());

        Assert.assertEquals(logMessage, logExpected);
    }

    @Test
    public void logWarning() throws Exception {
        Logger.warning("warn");

        LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
        LogMessage logExpected = new LogMessage("warn", Logger.LEVEL.WARNING.name());

        Assert.assertEquals(logMessage, logExpected);
    }

    @Test
    public void logInfo() throws Exception {
        Logger.info("info");

        LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
        LogMessage logExpected = new LogMessage("info", Logger.LEVEL.INFO.name());

        Assert.assertEquals(logMessage, logExpected);
    }

    @Test
    public void logDebug() throws Exception {
        Logger.debug("debug");

        LogMessage logMessage = gson.fromJson(out.toString(), LogMessage.class);
        LogMessage logExpected = new LogMessage("debug", Logger.LEVEL.DEBUG.name());

        Assert.assertEquals(logMessage, logExpected);
    }
}
