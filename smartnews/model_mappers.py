from smartnews.utils import format_news_date, format_news_field_field
from smartnews import const

# Convert News Feed APi object to Newsfeed Model
class NewsFeedMapper:
    def __init__(self, news_feed):
        self.post_title = news_feed['title'].strip()
        self.post_image = format_news_field_field(news_feed['urlToImage'])
        self.post_url = news_feed['url']
        self.post_source_name = news_feed['source']['name'].strip().replace(
            " ", "")
        self.post_source_logo = const.NEWS_AVATAR_BASE_URL + self.post_source_name
        self.post_summary = format_news_field_field(news_feed['description'])
        self.post_tags = news_feed['tags']
        self.post_date = format_news_date(news_feed['publishedAt'])

 