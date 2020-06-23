from smartnews.news_feeds_service import NewsFeedService
from flask_restx import Resource
from smartnews.apis.news_dto import NewsFeedDto


# get news feed api namespace dto
news_feeds_ns = NewsFeedDto.ns
news_feeds_model = NewsFeedDto.news_feeds


@news_feeds_ns.route('/page/<page_number>')
@news_feeds_ns.param('page', 'Page Number to get news feeds')
class NewsFeedResource(Resource):
    @news_feeds_ns.doc('Get a paginated list of news feeds by page number')
    @news_feeds_ns.marshal_list_with(news_feeds_model, envelope='data')
    def get(self, page_number):
        feeds = NewsFeedService.get_news_feeds(page_number)
        return feeds


@news_feeds_ns.route('/country/<country_id>')
@news_feeds_ns.param('country_id', 'News Feeds By country of origin')
class NewsFeedByCountryResource(Resource):
    @news_feeds_ns.doc('Get a paginated list of news feeds by country')
    @news_feeds_ns.marshal_list_with(news_feeds_model, envelope='data')
    def get(self, country_id):
        feeds = NewsFeedService.get_news_feeds_by_country(country_id, 1)
        return feeds
