package org.scrapy.scrapystreaming.messages;


import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.utils.Utils;

import java.lang.reflect.Field;
import java.util.List;

public abstract class Message {
    protected transient List<String> requiredFields = validator();

    public String sendMessage() throws SpiderException{
        validate();
        String message = Utils.gson.toJson(this);
        System.out.println(message);
        System.out.flush();

        return message;
    }

    public void validate() throws SpiderException {
        try {
            if (requiredFields != null) {
                for (String name : requiredFields) {
                    Field field = this.getClass().getField(name);
                    Object value = field.get(this);
                    if (value == null)
                        throw new SpiderException("Required field not provided: " + name);
                }
            }
        } catch (NoSuchFieldException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
    }

    public abstract List<String> validator();

    @Override
    public String toString() {
        return Utils.gson.toJson(this);
    }

    @Override
    public boolean equals(Object compare) {
        return this.toString().equals(compare.toString());
    }
}
