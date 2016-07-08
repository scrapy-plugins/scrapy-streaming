import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.Request;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import java.io.FileOutputStream;
import java.io.Writer;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.io.File;


/**
 * This is a simple example that shows that Scrapy Streaming is ready to handle utf8 webpages
 */
public class RequestUTF8 extends Spider {

    RequestUTF8() {
        name = "utf8";
        // opens a page with utf8 content
        start_urls.add("http://httpbin.org/encoding/utf8");
    }

    public void parse(ResponseMessage response) {
        try {
            // save the response body to a file
            File f = new File("outputs/utf8.html");
            Writer out = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(f), "UTF8"
            ));
            out.write(response.body);
            out.flush();
            out.close();
            close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String args[]) throws Exception {

        RequestUTF8 spider = new RequestUTF8();
        spider.start();
    }

}
