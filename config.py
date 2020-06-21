
from smartnews import const
# Hold all project configurations here

# Application secret key
SECRET_KEY = const.APP_SECRET_KEY

# Database configurations
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+const.DB_USER +':'+const.DB_PASSWORD+'@'+ const.DB_HOST + ':' + const.DB_PORT +'/smart_news'

SQLALCHEMY_TRACK_MODIFICATIONS = False
# Set debug 
DEBUG = True

# Set application thread to 2, one for handling requests and older for background
THREADS_PER_PAGE = 2