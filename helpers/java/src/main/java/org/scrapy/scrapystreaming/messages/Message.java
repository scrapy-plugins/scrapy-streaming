package org.scrapy.scrapystreaming.messages;


import org.scrapy.scrapystreaming.utils.Utils;

public class Message {

    public String sendMessage() {
        String message = this.toString();
        System.out.println(message);
        System.out.flush();

        return message;
    }

    @Override
    public String toString() {
        return Utils.gson.toJson(this);
    }

    @Override
    public boolean equals(Object compare) {
        return this.toString().equals(compare.toString());
    }
}
