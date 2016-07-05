package org.scrapy.scrapystreaming.core;


import org.scrapy.scrapystreaming.messages.ResponseMessage;


/**
 * Represents a callback function to handle a response
 */
public abstract class Callback {
    ResponseMessage response;

    /**
     * Set the response content
     * @param response response message
     */
    public void setResponse(ResponseMessage response) {
        this.response = response;
    }

    /**
     * Get the response content
     * @return resoponse data
     */
    public ResponseMessage getResponse() {
        return response;
    }

    /**
     * Method to handle to response content
     * @param response
     */
    public abstract void onResponse(ResponseMessage response);
}
