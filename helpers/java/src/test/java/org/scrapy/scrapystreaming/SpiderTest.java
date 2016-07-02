package org.scrapy.scrapystreaming;


import org.junit.Assert;
import org.junit.Test;
import org.scrapy.scrapystreaming.messages.CloseMessage;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.scrapy.scrapystreaming.messages.SpiderMessage;

import java.util.ArrayList;
import java.util.HashMap;

class TestSpider extends Spider {

    TestSpider(ArrayList<String> urls, ArrayList<String> domains, HashMap<String, String> settings) {
        name = "test";
        start_urls = urls;
        allowed_domains = domains;
        custom_settings = settings;
    }

    public void parse(ResponseMessage response) {

    }
}

public class SpiderTest extends BaseStd {

    @Test
    public void start() throws Exception {
        final ArrayList<String> urls = new ArrayList<String>(0);
        urls.add("http://example.com");
        urls.add("http://test.com");
        final ArrayList<String> domains = new ArrayList<String>(0);
        domains.add("example.com");
        domains.add("test.com");
        final HashMap<String, String> settings = new HashMap<String, String>(0);
        settings.put("setting 1", "value");
        settings.put("setting 2", "value");
        settings.put("setting 3", "value");

        new TestSpider(urls, domains, settings).start();

        SpiderMessage spider = gson.fromJson(out.toString(), SpiderMessage.class);
        SpiderMessage spiderExpected = new SpiderMessage();
        spiderExpected.name = "test";
        spiderExpected.start_urls = urls;
        spiderExpected.allowed_domains = domains;
        spiderExpected.custom_settings = settings;

        Assert.assertEquals(spiderExpected, spider);

        String json = "{\"type\":\"spider\",\"name\":\"test\",\"start_urls\":[\"http://example.com\"," +
                      "\"http://test.com\"],\"allowed_domains\":[\"example.com\",\"test.com\"]," +
                      "\"custom_settings\":{\"setting 1\":\"value\",\"setting 2\":\"value\",\"setting 3\":\"value\"}}";
        Assert.assertEquals(json.trim(), out.toString().trim());
    }

    @Test
    public void close() throws Exception {
        class TestSpider extends Spider{
            public void parse(ResponseMessage response) {}
        }
        TestSpider spider = new TestSpider();
        spider.start();
        out.reset();
        spider.close();

        CloseMessage close = gson.fromJson(out.toString(), CloseMessage.class);
        CloseMessage closeExpected = new CloseMessage();

        Assert.assertEquals(close, closeExpected);

        String json = "{\"type\":\"close\"}";
        Assert.assertEquals(json.trim(), out.toString().trim());
    }
}
