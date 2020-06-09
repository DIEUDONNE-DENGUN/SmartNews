from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create a flask app
app = Flask(__name__)

# set app configuration and MYSQL database setting from config file
app.config.from_object('config')

# create database ORM instance
db = SQLAlchemy(app)

# inittiate and run all background cron tasks to pull news from news api and crawler
from smartnews import background_tasks

# import api routes
from smartnews import routes



