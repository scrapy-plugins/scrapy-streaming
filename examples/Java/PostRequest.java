import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.Logger;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.Request;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.scrapy.scrapystreaming.messages.FromResponseMessage;
import org.scrapy.scrapystreaming.utils.Utils;
import java.io.Writer;
import java.io.FileWriter;
import java.util.HashMap;


/**
 * This is a sample spider to demonstrate how to use a request with POST.
 */
public class PostRequest extends Spider {

    PostRequest() {
        name = "post";
    }

    public void parse(ResponseMessage response) {
    }

    public static void main(String args[]) throws Exception {
        PostRequest spider = new PostRequest();
        spider.start();
        // open the request
        Request req = new Request("http://httpbin.org/post");
        req.method = "POST";
        req.body = "Post Body";
        req.open(new Callback() {
            public void parse(ResponseMessage response) {
                try {
                    Writer writer = new FileWriter("outputs/post.json");
                    Utils.gson.toJson(response.body, writer);
                    writer.flush();
                } catch (Exception e) {
                    e.printStackTrace();
                }
                spider.close();
            }
        });
    }

}
