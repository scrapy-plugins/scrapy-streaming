package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.messages.RequestMessage;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.utils.Utils;


public class Request extends RequestMessage {

    public Request(String url) {
        this.url = url;
    }

    public void open(Callback callback) throws SpiderException {
        String id = this.id;
        if (id == null)
            id = callback.toString();
        this.id = id;
        Utils.responseMapping.put(id, callback);

        sendMessage();
    }
}
