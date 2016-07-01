package org.scrapy.scrapystreaming;

import org.scrapy.scrapystreaming.core.CommunicationProtocol;
import org.scrapy.scrapystreaming.messages.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


public abstract class Spider {
    public String name = "ExternalSpider";
    public List<String> start_urls = new ArrayList<String>(0);
    public List<String> allowed_domains;
    public HashMap<String, String> custom_settings;
    protected boolean isRunning = false;
    protected CommunicationProtocol protocol;


    public final void start() throws Exception {
        if (isRunning)
            throw new Exception("Spider already running");

        new SpiderMessage(name, start_urls, allowed_domains, custom_settings).sendMessage();
        protocol = new CommunicationProtocol();
        protocol.start();

        isRunning = true;
    }

    public void close() {
        new CloseMessage().sendMessage();
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