package org.scrapy.scrapystreaming.utils;


import com.google.gson.Gson;
import org.scrapy.scrapystreaming.core.Callback;

import java.util.HashMap;

public class Utils {
    public static Gson gson = new Gson();
    public static HashMap<String, Callback> responseMapping = new HashMap<String, Callback>(0);
}
