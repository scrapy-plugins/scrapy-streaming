package org.scrapy.scrapystreaming;

import org.scrapy.scrapystreaming.core.CommunicationProtocol;
import org.scrapy.scrapystreaming.messages.*;
import org.scrapy.scrapystreaming.core.SpiderException;


public abstract class Spider extends SpiderMessage {
    protected transient boolean isRunning = false;
    protected transient CommunicationProtocol protocol;

    public final void start() throws Exception {
        if (isRunning)
            throw new Exception("Spider already running");

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

}

class Teste extends Spider {

    public void parse(ResponseMessage response) {

    }

    public static void main (String args[]) throws Exception {
        new Teste().start();
    }
}