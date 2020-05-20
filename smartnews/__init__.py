from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# create a flask app
app = Flask(__name__)
# set app configuration and MYSQL database setting
app.config['SECRET_KEY'] ='33191185783744c6a127b20c396a67fb'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost:3306/smart_news'
db = SQLAlchemy(app)

# inittiate and run all background cron tasks to pull news from news api and crawler
from smartnews import background_tasks

# import api routes
from smartnews import routes



