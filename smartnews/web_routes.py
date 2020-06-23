from smartnews.news_feeds_service import NewsFeedService
from flask_restx import Resource
from smartnews import app


# Web routes here to render web views through a Jinga template

@app.route('/')
def showHomePage():
    return 'Welcome to smar news web portal'
