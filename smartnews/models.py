from datetime import datetime
from smartnews import db


class NewsFeeds(db.Model):
    __tablename__ = "news_feeds"
    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(255), nullable=False)
    post_image_url = db.Column(db.String(200), nullable=False)
    post_summary = db.Column(db.Text, nullable=False)
    post_source_id = db.Column(
        db.Integer, db.ForeignKey('news_sources.id'), nullable=False)
    post_country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    post_date = db.Column(db.String(25), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class NewsSources(db.Model):
    __tablename__ = "news_sources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class NewsTags(db.Model):
    __tablename__ = "news_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class NewsTagPivot(db.Model):
    __tablename__ = "news_tags_pivot"
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, nullable=False)
    tag_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


class Country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=True)
# db.create_all()
