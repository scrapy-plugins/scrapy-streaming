import org.scrapy.scrapystreaming.Spider;
import org.scrapy.scrapystreaming.Logger;
import org.scrapy.scrapystreaming.core.Callback;
import org.scrapy.scrapystreaming.FromResponseRequest;
import org.scrapy.scrapystreaming.messages.ResponseMessage;
import org.scrapy.scrapystreaming.messages.FromResponseMessage;
import java.util.HashMap;


/**
 * This is a sample spider to demonstrate how to use the FromResponseRequest.
 * It initialy opens the github login page, and the post the user login data in the login form;
 */
public class GithubLogin extends Spider {

    GithubLogin() {
        name = "login";
    }

    public void parse(ResponseMessage response) {
    }

    public static void main(String args[]) throws Exception {
        GithubLogin spider = new GithubLogin();
        spider.start();

        // put the login data in a map
        HashMap<String, String> loginData = new HashMap<String, String>(0);
        loginData.put("login", "email@example.com");
        loginData.put("password", "pass");

        // adds the formdata paramenter with the login information
        FromResponseMessage data = new FromResponseMessage();
        data.formdata = loginData;

        // open the request
        FromResponseRequest req = new FromResponseRequest("https://github.com/login", data);
        req.open(new Callback() {
            public void onResponse(ResponseMessage response) {

                // validate if the loggin was correct or not
                if (response.body.contains("Incorrect username or password")) {
                    Logger.debug("Incorrect username or password");
                } else {
                    Logger.debug("Login correct!");
                }
                spider.close();
            }
        });
    }

}
