import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.Request;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.apache.commons.codec.binary.Base64;
import java.io.FileOutputStream;
import java.io.File;


/**
 * This examples demonstrate how to download binary data using Scrapy Streaming.
 *
 * It downloads an image using base64, and then save it to a file.
 */
public class RequestImage extends Spider {

    RequestImage() {
        name = "image";
    }

    public void parse(ResponseMessage response) {

    }

    public static void main(String args[]) throws Exception {

        RequestImage spider = new RequestImage();
        spider.start();

        // open a request to download the image
        Request r = new Request("http://httpbin.org/image/png");
        // set the body encoding to base64, so it can download the image using json
        r.base64 = true;

        r.open(new Callback() {
            public void onResponse(ResponseMessage response) {
                try {
                    // write the response body to a file and close the spider
                    byte data[] = Base64.decodeBase64(response.body);
                    FileOutputStream img = new FileOutputStream(new File("outputs/image.png"));
                    img.write(data);
                    img.close();
                    spider.close();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

    }

}
