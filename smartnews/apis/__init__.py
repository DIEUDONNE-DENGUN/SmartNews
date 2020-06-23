from flask import Blueprint
from flask_restx import Api
from smartnews.const import API_PREFIX_1

# set api routing blueprint
blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX_1)
# set api route initiallization
api_v1 = Api(blueprint,
             title='News Feeds Aggregator restful api service',
             version='1.0',
             description='Api for providing news feeds from smart news'
             )

# add api namesaces to the Main APi object
from smartnews.apis.news_feeds_ns import news_feeds_ns as ns1
api_v1.add_namespace(ns1)
