from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# create a flask app
app = Flask(__name__)
# set app configuration and database
app.config['SECRET_KEY'] ='33191185783744c6a127b20c396a67fb'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/smart_news'
db = SQLAlchemy(app)

from smartnews.webcrawler import WebCrawler
from smartnews.models import NewsFeeds

# run webcrawler class to scrape and save news feed to db
def run_webcrawler():
    web_scrapper = WebCrawler()
    web_scrapper.run_webcrawler_headlines() #news headlines from homepage
    news_feeds = web_scrapper.get_all_news_scraped()
    for news_feed in news_feeds:
        news_feed_object = NewsFeeds()
        news_feed_object.save_news_feeds(news_feed)
        # print(news_feed_saved)


# Run app scheduler to start scraping data from daily news
scheduler = BackgroundScheduler()
scheduler.start()
job = scheduler.add_job(run_webcrawler, 'interval', minutes=2)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# import api routes
from smartnews import routes



