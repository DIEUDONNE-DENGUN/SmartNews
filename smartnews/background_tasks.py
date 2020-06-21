
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import logging
import os
from smartnews import app
from smartnews.webcrawler import WebCrawler
from smartnews.news_org_api_service import NewsOrgApiService

# run webcrawler class to scrape and save news feed to db

os.environ['TZ'] = 'Africa/Douala'

def run_webcrawler():
    # create a webcrawler instance and run scraper
    print("Running Web Crawler Task:")
    web_scrapper = WebCrawler()
    web_scrapper.run_webcrawler_headlines()  # news headlines from homepage
    news_feeds = web_scrapper.save_all_news_db()


def get_news_from_news_api():
    # create a news org service instance
    print("Running NewsApi Service Task:")
    news_api_service = NewsOrgApiService()
    # get general news headlines
    news_api_service.get_top_news_headlines_by_general()


# Run app scheduler to start scraping data from daily news
scheduler = BackgroundScheduler()
job_store_url = app.config['SQLALCHEMY_DATABASE_URI']
# set up jobstore as DB store
scheduler.add_jobstore('sqlalchemy', url=job_store_url)

# add web crawling news task to scheduler
# scheduler.add_job(run_webcrawler, 'interval', minutes=5)
# add an another job to start getting news feeds from newsorg
scheduler.add_job(get_news_from_news_api, 'interval', minutes=2)
# start scheduler
scheduler.start()
# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())

# Add logging to monitor app scheduler, for debugging purposes
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
