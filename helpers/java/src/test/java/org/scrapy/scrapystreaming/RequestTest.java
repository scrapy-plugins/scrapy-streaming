package org.scrapy.scrapystreaming;


import org.junit.Assert;
import org.junit.Test;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.ResponseMessage;

public class RequestTest extends BaseStd {

    @Test
    public void openGeneratesID() throws SpiderException {
        Request r = new Request("http://example.com");
        Assert.assertEquals(r.id, null);

        r.open(new Callback() {
            @Override
            public void parse(ResponseMessage response) {
                //
            }
        });

        Assert.assertNotEquals(r.id, null);
    }

    @Test
    public void openKeepsID() throws SpiderException {
        Request r = new Request("http://example.com");
        r.id = "test";

        r.open(new Callback() {
            @Override
            public void parse(ResponseMessage response) {
                //
            }
        });

        Assert.assertEquals(r.id, "test");
    }
}
