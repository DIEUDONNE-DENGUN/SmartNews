from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api

# create a flask app
app = Flask(__name__)

# set app configuration and MYSQL database setting from config file
app.config.from_object('config')

# create database ORM instance
db = SQLAlchemy(app)

# set api route initiallization
api = Api(app,
          title='News Feeds Aggregator restful api service',
          version='1.0',
          description='Api for providing news feeds from smart news'
          )

# initiate and run all background cron tasks to pull news from news api and crawler
from smartnews import background_tasks
# import api initialized routes
from smartnews import routes



