package org.scrapy.scrapystreaming.core;


import org.scrapy.scrapystreaming.messages.ResponseMessage;


/**
 * Represents a callback function to handle a response
 */
public interface Callback {

    /**
     * Method to handle to response content
     * @param response
     */
    public void parse(ResponseMessage response);
}
