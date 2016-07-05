package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.FromResponseMessage;
import org.scrapy.scrapystreaming.messages.FromResponseRequestMessage;
import org.scrapy.scrapystreaming.utils.Utils;

public class FromResponseRequest extends FromResponseRequestMessage{

    public FromResponseRequest(String url, FromResponseMessage from_response_request) {
        this.url = url;
        this.from_response_request = from_response_request;
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
