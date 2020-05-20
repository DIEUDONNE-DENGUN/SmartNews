from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from smartnews import const

# create a flask app
app = Flask(__name__)
# set app configuration and MYSQL database setting
app.config['SECRET_KEY'] = const.APP_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://'+const.DB_USER +':'+const.DB_PASSWORD+'@'+ const.DB_HOST + ':' + const.DB_PORT +'/smart_news'
db = SQLAlchemy(app)

# inittiate and run all background cron tasks to pull news from news api and crawler
from smartnews import background_tasks

# import api routes
from smartnews import routes



