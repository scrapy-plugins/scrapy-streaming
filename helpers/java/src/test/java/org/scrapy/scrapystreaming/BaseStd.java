package org.scrapy.scrapystreaming;


import com.google.gson.Gson;
import org.junit.Before;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

public class BaseStd {
    ByteArrayOutputStream out;
    Gson gson = new Gson();

    @Before
    public void setUp() {
        out = new ByteArrayOutputStream();
        System.setOut(new PrintStream(out));
    }

}
