package org.scrapy.scrapystreaming;

import org.scrapy.scrapystreaming.core.CommunicationProtocol;
import org.scrapy.scrapystreaming.messages.*;
import org.scrapy.scrapystreaming.core.SpiderException;


/**
 * This class lets you create the External Spider and run / stop it.
 */
public abstract class Spider extends SpiderMessage {
    private transient boolean isRunning = false;
    private transient CommunicationProtocol protocol;

    /**
     * Start the Spider execution
     * @throws SpiderException
     */
    public final void start() throws SpiderException {
        if (isRunning)
            throw new SpiderException("Spider already running");

        sendMessage();
        protocol = new CommunicationProtocol(this);
        protocol.start();

        isRunning = true;
    }

    /**
     * Stop the spider execution, sending the close message.
     * The process will be killed as soon as Scrapy Streaming receives this message.
     */
    public void close() {
        try {
            new CloseMessage().sendMessage();
        } catch (SpiderException e) {
            e.printStackTrace();
        }
    }

    /**
     * The callback of initial_urls responses.
     * @param response response data
     */
    public abstract void parse(ResponseMessage response);

    /**
     * This method is called when Scrapy raises an exception and sends the exception message.
     * If you want to analyze the exception, or just ignore the problem, override this function.
     * @param exception exception message sent by Scrapy Streaming
     * @throws SpiderException
     */
    public void onException(ExceptionMessage exception) throws SpiderException {
        throw new SpiderException("Scrapy raised an exception. Message sent: " + exception.received_message +
                "; Exception message: " + exception.exception);
    }

}