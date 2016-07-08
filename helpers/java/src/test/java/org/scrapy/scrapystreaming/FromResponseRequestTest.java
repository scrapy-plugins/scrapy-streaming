package org.scrapy.scrapystreaming;


import org.junit.Assert;
import org.junit.Test;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.FromResponseMessage;
import org.scrapy.scrapystreaming.messages.ResponseMessage;

public class FromResponseRequestTest extends BaseStd {

    @Test
    public void openGeneratesID() throws SpiderException {
        FromResponseMessage fromResponseMessage = new FromResponseMessage();
        FromResponseRequest r = new FromResponseRequest("http://example.com", fromResponseMessage);
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
        FromResponseMessage fromResponseMessage = new FromResponseMessage();
        FromResponseRequest r = new FromResponseRequest("http://example.com", fromResponseMessage);
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
