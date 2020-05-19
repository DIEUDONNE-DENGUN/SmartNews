from smartnews import app
from flask import jsonify
# from smartnews.webcrawler import WebCrawler
# from smartnews.models import NewsFeeds

@app.route("/", methods=['GET'])
def top_kamer_news_feeds():
    # Run app scheduler to start scraping data from daily news
    # run webcrawler class
    # web_scrapper = WebCrawler()
    # web_scrapper.run_webcrawler_headlines() #news headlines from homepage
    # news_feeds = web_scrapper.get_all_news_scraped()
    # for news_feed in news_feeds:
    #     news_feed_object = NewsFeeds()
    #     news_feed_saved = news_feed_object.save_news_feeds(news_feed)
         
    # dump(news_feeds)
    return "Hello Home Page"