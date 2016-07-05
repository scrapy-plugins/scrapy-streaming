package org.scrapy.scrapystreaming.core;


import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.messages.*;
import org.scrapy.scrapystreaming.utils.Utils;

import java.io.*;

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
                line = line.trim();
                if (line.length() > 0) {
                    ReceivedMessage msg = Utils.gson.fromJson(line, ReceivedMessage.class);
                    messageReceived(msg, line);
                }
            } catch (IOException e) {
                System.err.println("There is a problem in the communication channel: " + e.getMessage());
            } catch (SpiderException e) {
                System.err.println(e.getMessage());
            }
        }
    }

    protected void messageReceived(ReceivedMessage msg, String line) throws SpiderException {
        if (msg.type.equals("ready")) {
            ReadyMessage status = Utils.gson.fromJson(line, ReadyMessage.class);
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
        } else {
            throw new SpiderException("Invalid message type: " + msg.type);
        }
    }

    protected void onStatus(ReadyMessage status) throws SpiderException {
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

    protected void onException(ExceptionMessage exception) throws SpiderException {
        spider.onException(exception);
    }

    protected void onError(ErrorMessage error) throws SpiderException {
        throw new SpiderException("Spider error. Message sent: " + error.received_message +
                "; Error details: " + error.details);
    }
}
