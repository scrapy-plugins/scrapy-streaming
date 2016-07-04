package org.scrapy.scrapystreaming;

import org.scrapy.scrapystreaming.core.CommunicationProtocol;
import org.scrapy.scrapystreaming.messages.*;
import org.scrapy.scrapystreaming.core.SpiderException;


public abstract class Spider extends SpiderMessage {
    protected transient boolean isRunning = false;
    protected transient CommunicationProtocol protocol;

    public final void start() throws SpiderException {
        if (isRunning)
            throw new SpiderException("Spider already running");

        sendMessage();
        protocol = new CommunicationProtocol(this);
        protocol.start();

        isRunning = true;
    }

    public void close() {
        try {
            new CloseMessage().sendMessage();
        } catch (SpiderException e) {
            e.printStackTrace();
        }
    }

    public abstract void parse(ResponseMessage response);

    public void onException(ExceptionMessage exception) throws SpiderException {
        throw new SpiderException("Scrapy raised an exception. Message sent: " + exception.received_message +
                "; Exception message: " + exception.exception);
    }

}