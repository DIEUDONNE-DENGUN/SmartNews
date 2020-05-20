
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging
from smartnews.webcrawler import WebCrawler
from smartnews.models import NewsFeeds
from smartnews.news_org_api_service import NewsOrgApiService

# run webcrawler class to scrape and save news feed to db


def run_webcrawler():
    web_scrapper = WebCrawler()
    web_scrapper.run_webcrawler_headlines()  # news headlines from homepage
    news_feeds = web_scrapper.get_all_news_scraped()
    for news_feed in news_feeds:
        news_feed_object = NewsFeeds()
        news_feed_object.save_news_feeds(news_feed)
        # print(news_feed_saved)


def get_news_from_news_api():
    # create a news org service instance
    news_api_service = NewsOrgApiService()
    # get general news headlines
    news_api_service.get_top_news_headlines_by_general()


# Run app scheduler to start scraping data from daily news
scheduler = BackgroundScheduler()
scheduler.start()
# add web crawling news task to scheduler
scheduler.add_job(run_webcrawler, 'interval', minutes=2)
# add an another job to start getting news feeds from newsorg
scheduler.add_job(get_news_from_news_api, 'interval', minutes=2)


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Add logging to monitor app scheduler, for debugging purposes
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
