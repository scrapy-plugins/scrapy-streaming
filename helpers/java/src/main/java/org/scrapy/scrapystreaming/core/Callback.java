package org.scrapy.scrapystreaming.core;


import org.scrapy.scrapystreaming.messages.ResponseMessage;


public abstract class Callback {
    ResponseMessage response;

    public void setResponse(ResponseMessage response) {
        this.response = response;
    }

    public ResponseMessage getResponse() {
        return response;
    }

    public abstract void onResponse(ResponseMessage response);
}
