import java.util.HashMap;
import java.io.Writer;
import java.io.FileWriter;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.scrapy.scrapystreaming.Request;
import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.utils.Utils;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.core.SpiderException;
import org.scrapy.scrapystreaming.messages.ResponseMessage;


/**
 * This spider is covered in the quickstart section.
 *
 * This scrape the dmoz webpage, looking for Python websites
 */
public class Dmoz extends Spider {
    // we use the numRequests to count remaining requests
    static int numRequests = 0;
    // the results variable store the extracted data, mapping from title: url
    static HashMap<String, String> results = new HashMap<String, String>(0);

    Dmoz() {
        name = "dmoz";
        // set the initial url
        start_urls.add("http://www.dmoz.org/Computers/Programming/Languages/Python/");
    }

    public void parse(ResponseMessage response) {
        // get the intal page, and open a new request to each subcategory
        Document doc = Jsoup.parse(response.body);
        Elements hrefs = doc.select("#subcategories-div > section > div > div.cat-item > a[href]");
        for (Element el: hrefs) {
            try {
                Request r = new Request("http://www.dmoz.org" + el.attr("href"));
                r.open(new Callback() {
                    public void onResponse(ResponseMessage response) {
                        parseSubcat(response);
                    }
                });

                // increments the number of open requests
                numRequests++;
            } catch (SpiderException e) {
                e.printStackTrace();
            }
        }
    }

    public void parseSubcat(ResponseMessage response) {
        // decrement the number of open requests
        numRequests--;
        Document doc = Jsoup.parse(response.body);
        Elements divs = doc.select("div.title-and-desc a");

        // extract all urls in the page
        for (Element item: divs) {
            String url = item.attr("href");
            String title = item.select("div.site-title").first().text();
            results.put(title, url);
        }

        // close the spider and save the data, when necessary
        if (numRequests == 0) {
            try {
                Writer writer = new FileWriter("outputs/dmoz.json");
                Utils.gson.toJson(results, writer);
                writer.flush();
            } catch (Exception e) {
                e.printStackTrace();
            }
            close();
        }

    }

    public static void main(String args[]) throws Exception {
        Dmoz spider = new Dmoz();
        spider.start();
    }
}
