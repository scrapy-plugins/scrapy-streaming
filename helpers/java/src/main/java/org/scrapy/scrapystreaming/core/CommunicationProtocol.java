package org.scrapy.scrapystreaming.core;


import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.messages.*;
import org.scrapy.scrapystreaming.utils.Utils;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class CommunicationProtocol extends Thread {
    BufferedReader in;
    Spider spider;

    public CommunicationProtocol(Spider spider) {
        this.spider = spider;
        in = new BufferedReader(new InputStreamReader(System.in));
    }

    @Override
    public void run() {
        while (true) {
            try {
                String line = in.readLine();
                ReceivedMessage msg = Utils.gson.fromJson(line, ReceivedMessage.class);

                messageReceived(msg, line);
            } catch (IOException e) {
                System.err.println("There is a problem in the communication channel: " + e.getMessage());
            } catch (SpiderException e) {
                System.err.println(e.getMessage());
            }
        }
    }

    protected void messageReceived(ReceivedMessage msg, String line) throws SpiderException {
        if (msg.type.equals("status")) {
            StatusMessage status = Utils.gson.fromJson(line, StatusMessage.class);
            onStatus(status);
        } else if (msg.type.equals("response")) {
            ResponseMessage response = Utils.gson.fromJson(line, ResponseMessage.class);
            onResponse(response);
        } else if (msg.type.equals("exception")) {
            ExceptionMessage exception = Utils.gson.fromJson(line, ExceptionMessage.class);
            onException(exception);
        } else if (msg.type.equals("error")) {
            ErrorMessage error = Utils.gson.fromJson(line, ErrorMessage.class);
            onError(error);
        }
    }

    protected void onStatus(StatusMessage status) throws SpiderException {
        if (!status.status.equals("ready")) {
            throw new SpiderException("There is a problem in the communication channel. Received status: " + status.status);
        }
    }

    protected void onResponse(ResponseMessage response) {
        if (response.id.equals("parse")) {
            spider.parse(response);
        } else {
            Utils.responseMapping.get(response.id).onResponse(response);
        }
    }

    protected void onException(ExceptionMessage exception) {

    }

    protected void onError(ErrorMessage error) {

    }
}
