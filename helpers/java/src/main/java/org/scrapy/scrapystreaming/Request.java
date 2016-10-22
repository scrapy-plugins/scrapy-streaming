package org.scrapy.scrapystreaming;


import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.messages.RequestMessage;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.utils.Utils;

/**
 * Open a new request
 */
public class Request extends RequestMessage {

    /**
     * Creates the request object, passing its url
     * @param url request URL
     */
    public Request(String url) {
        this.url = url;
    }

    /**
     * Open the request given its callback.
     * The callback function will be called with the response as soon as it's available.
     * @param callback response callback
     * @throws SpiderException
     */
    public void open(Callback callback) throws SpiderException {
        String id = this.id;
        if (id == null)
            id = callback.toString();
        this.id = id;
        Utils.responseMapping.put(id, callback);

        sendMessage();
    }
}
