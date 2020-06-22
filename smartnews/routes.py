from smartnews.news_feeds_service import NewsFeedService
from flask_restx import Resource
from smartnews.news_dto import NewsFeedDto


# get news feed api namespace dto
ns = NewsFeedDto.ns
news_feeds = NewsFeedDto.news_feeds


@ns.route('/page/<page_number>')
@ns.param('page', 'Page Number to get news feeds')
class NewsFeedResource(Resource):
    @ns.doc('Get a paginated list of news feeds by page number')
    @ns.marshal_list_with(news_feeds, envelope='data')
    def get(self, page_number):
        feeds = NewsFeedService.get_news_feeds(page_number)
        return feeds


@ns.route('/country/<country_id>')
@ns.param('country_id', 'News Feeds By country of origin')
class NewsFeedByCountryResource(Resource):
    @ns.doc('Get a paginated list of news feeds by country')
    @ns.marshal_list_with(news_feeds, envelope='data')
    def get(self, country_id):
        feeds = NewsFeedService.get_news_feeds_by_country(country_id, 1)
        return feeds
