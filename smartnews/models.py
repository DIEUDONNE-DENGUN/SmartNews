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

    def save_news_feeds(self, news_feed):
        
        # check if we previously had a news with feeds by title
        news_feed_exist = self.news_feed_exist_by_name(news_feed['post_title'])
        if news_feed_exist:
            return ""
        # News feed is a new one, save it and its details in the db
        self.post_title = news_feed['post_title'].strip()
        self.post_image_url = news_feed['post_image']
        self.post_summary = news_feed['post_summary']
        self.post_url = news_feed['post_url']
        self.post_source_id = NewsSources().get_news_source_id_by_name(
            news_feed)  # Find news_feed source by id
        self.post_country_id = 1
        self.post_date = news_feed['post_date']
        self.created_at = datetime.now()
        # save the news feed main data
        db.session.add(self)
        db.session.commit()
        # save the created news feed and its associated tags
        self.save_news_tags_pivot(self.id, news_feed['post_tags'])
        return "saved"

    def save_news_tags_pivot(self, news_id, news_tags):
        news_id = news_id
        # save all current news_feed tags to db and retun their ids
        news_tags_id = NewsTags().save_news_tag(news_tags)
        # Loop through list ids and save in pivot table for
        for tag_id in news_tags_id:
            # create a news_tag_pivot row to track news feed and tags table
            news_tags_pivot = NewsTagPivot(
                news_id=news_id, tag_id=tag_id, created_at=datetime.now())
            db.session.add(news_tags_pivot)
        # commit all tags pivot to db pivot table
        db.session.commit()

    # check if a news feed about to be saved exist already by
    def news_feed_exist_by_name(self, news_feed):
        feeds_exist = False
        news_feed_exist = NewsFeeds.query.filter_by(post_title=news_feed).first()
        if news_feed_exist:
            feeds_exist = True
        return feeds_exist


class NewsSources(db.Model):
    __tablename__ = "news_sources"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(150), nullable=False)
    domain = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def get_news_source_id_by_name(self, news_feed):
        # get news source by name if exist, if not, create a new one and return id
        source_name = news_feed['post_source_name'].strip()
        source_logo = news_feed['post_source_logo'].strip()
        source_exist = NewsSources.query.filter_by(logo=source_logo).first()
        if source_exist:
            return source_exist.id
        # create a new source and return id
        source = NewsSources(name=source_name, logo=source_logo,
                             domain='', created_at=datetime.now())
        db.session.add(source)
        db.session.commit()
        return source.id


class NewsTags(db.Model):
    __tablename__ = "news_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def get_news_tag_id_by_name(self, tag):
        tag_id = 0
        tag_exist = NewsTags.query.filter_by(name=tag).first()
        if tag_exist:
            tag_id = tag_exist.id
        return tag_id

    def save_news_tag(self, news_tags):
        # Save list of tags  and retun ids
        tag_list_ids = []
        for tag in news_tags:
            # check if tag exist, return it or create a new one
            tag_exist_id = self.get_news_tag_id_by_name(tag)
            if tag_exist_id > 0:
                tag_list_ids.append(tag_exist_id)
            else:
                # create a new tag and return its id instead, doesn't exist
                new_tag = NewsTags(name=tag, created_at=datetime.now())
                db.session.add(new_tag)
                db.session.commit()
                tag_list_ids.append(new_tag.id)
                
        return tag_list_ids


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
