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
 * This is a sample spider that navigates in the scrapy-plugins organization, and
 * extract information about all scrapy-plugins' repositories
 */
public class Github extends Spider {
    // count the number of requests
    static int numRequests = 0;
    // save the data, mapping from repo name: repo data
    static HashMap<String, HashMap<String, String>> results = new HashMap<String, HashMap<String, String>>(0);

    Github() {
        name = "github";
        start_urls.add("https://github.com/scrapy-plugins");
    }

    public void parse(ResponseMessage response) {
        Document doc = Jsoup.parse(response.body);
        Elements hrefs = doc.select("h3.repo-list-name > a[href]");

        // iterate and open a request to the page of each repository
        for (Element el: hrefs) {
            try {
                Request r = new Request("https://github.com" + el.attr("href"));
                r.open(new Callback() {
                    public void parse(ResponseMessage response) {
                        parseRepo(response);
                    }
                });

                // adds the number of open requests
                numRequests++;
            } catch (SpiderException e) {
                e.printStackTrace();
            }
        }
    }

    public void parseRepo(ResponseMessage response) {
        // decrement the number of open requests
        numRequests--;
        Document doc = Jsoup.parse(response.body);

        // extract the repo data
        String title = doc.select("h1.public strong a").first().text();
        String stars = doc.select("a.social-count").get(1).text();
        String issues = doc.select("span.counter").get(0).text();
        String pr = doc.select("span.counter").get(1).text();

        HashMap<String, String> repo = new HashMap<String, String>(0);
        repo.put("title", title);
        repo.put("stars", stars);
        repo.put("issues", issues);
        repo.put("pr", pr);
        results.put(title, repo);

        // save the data and close the spider when necessary
        if (numRequests == 0) {
            try {
                Writer writer = new FileWriter("outputs/github.json");
                Utils.gson.toJson(results, writer);
                writer.flush();
            } catch (Exception e) {
                e.printStackTrace();
            }
            close();
        }
    }

    public static void main(String args[]) throws Exception {
        Github spider = new Github();
        spider.start();
    }
}
