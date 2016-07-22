import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.Logger;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.FromResponseRequest;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.scrapy.scrapystreaming.messages.FromResponseMessage;
import org.scrapy.scrapystreaming.utils.Utils;
import java.io.Writer;
import java.io.FileWriter;
import java.util.HashMap;


/**
 * This is a sample spider to demonstrate how to use the FromResponseRequest.
 */
public class FillForm extends Spider {

    FillForm() {
        name = "form";
    }

    public void parse(ResponseMessage response) {
    }

    public static void main(String args[]) throws Exception {
        FillForm spider = new FillForm();
        spider.start();

        // put the form data in a map
        HashMap<String, String> formData = new HashMap<String, String>(0);
        formData.put("custname", "Sample");
        formData.put("custemail", "email@example.com");

        // adds the formdata paramenter with the form information
        FromResponseMessage data = new FromResponseMessage();
        data.formdata = formData;

        // open the request
        FromResponseRequest req = new FromResponseRequest("http://httpbin.org/forms/post", data);
        req.open(new Callback() {
            public void parse(ResponseMessage response) {
                try {
                    Writer writer = new FileWriter("outputs/fill_form.json");
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
