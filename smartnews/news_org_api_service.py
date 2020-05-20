# Handle getting of latest news updates from NewsOrg Api

import requests
import json
import jsons
from smartnews import const
from smartnews.utils import format_news_date
from smartnews.models import NewsFeeds


class NewsOrgApiService:
    def __init__(self):
        self.api_base_url = const.NEWS_ORG_API_BASE_URL
        self.api_key = const.NEWS_ORG_API_KEY
        self.request_client = requests

    # Get authorization header for NewsOrg API service
    def get_request_authoriation_header(self):
        request_header = {"Content-Type": "application/json",
                          "Authorization": self.api_key}
        return request_header

    def parse_news_api_response(self, response):
        # print(response)
        news_feeds_list = []
        # check if there news feeds
        # data = response
        news_feeds_count = response['totalResults']
        if news_feeds_count > 0:
            # cconvert json data into python dict
            api_news_feeds = json.loads(response['articles'])
            news_tags = [const.NEWS_ORG_API_CATEGORIES[0]]
            # loop through the dicts of news feeds
            for news_feed in api_news_feeds:
                news_feed_object = jsons.dump(NewsFeed(news_feed, news_tags))
                news_feeds_list.append(news_feed_object)
                print(news_feed_object)

        return news_feeds_list

    def save_news_feeds_db(self, news_feeds_list):
        # Loop through news feeds list of dicts
        for news_feed in news_feeds_list:
            # Save to news feed to database
            news_feed_db_instance = NewsFeeds()
            news_feed_db_instance.save_news_feeds(news_feed,2)

    # Get top headlines as a general category

    def get_top_news_headlines_by_general(self):
        api_service_url = self.api_base_url + "top-headlines"
        api_service_params = {
            "category": const.NEWS_ORG_API_CATEGORIES[0], "country": const.NEWS_ORG_API_DEFAULT_COUNTRY}
        # try to connect to the news api service

        try:
            request = self.request_client.get(
                api_service_url, params=api_service_params, headers=self.get_request_authoriation_header())
            request.raise_for_status()
            response_json = request.json()
            news_feeds_list = self.parse_news_api_response(response_json)
            # save news feed to db
            self.save_news_feeds_db(news_feeds_list)
            
        except self.request_client.exceptions.HTTPError as http_error:
            print(http_error.response.text)


# News feed
class NewsFeed:
    def __init__(self, news_feed, tags):
        self.post_title = news_feed['title'].strip()
        self.post_image = news_feed['urlToImage']
        self.post_url = news_feed['url']
        self.post_source_name = news_feed['source']['name'].strip().replace(
            " ", "")
        self.post_source_logo = const.NEWS_AVATAR_BASE_URL + self.post_source_name
        self.post_summary = news_feed['description']
        self.post_tags = tags
        self.post_date = format_news_date(news_feed['publishedAt'])
