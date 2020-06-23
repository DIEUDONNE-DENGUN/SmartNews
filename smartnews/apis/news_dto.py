from flask_restx import Namespace, fields
from smartnews.apis import api_v1
from smartnews.news_feeds_service import NewsFeedService

# Custom dto to pull all associated tags for each news feed


class NewsTagsDto(fields.Raw):
    def format(self, feed_id):
        news_feed_tags = NewsFeedService.get_news_feed_tags_by_id(feed_id)
        return news_feed_tags


class NewsFeedDto:
    ns = api_v1.namespace('news_feeds',
                          description='News Feeds related operations')
    news_feeds = api_v1.model('NewsFeeds', {
        'title': fields.String(required=True, attribute='post_title', description='news feed title'),
        'feature_image_url': fields.String(required=True, attribute='post_image_url',
                                           description='news feed feature image url'),
        'summary': fields.String(required=True, attribute='post_summary', description='news feed summary text'),
        'url': fields.String(attribute='post_url', description='Link to the news feed for details'),
        'source': fields.String(attribute='source.name', description='news feed source name'),
        'source_logo': fields.String(attribute='source.logo', description='news feed source logo'),
        'tags': NewsTagsDto(attribute='id'),
        'post_date': fields.String(required=True, attribute='created_at', description='news feed date of creation'),
    })
